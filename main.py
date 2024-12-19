import requests
import urllib.parse
import time
from datetime import datetime, timedelta
import random
from rich.console import Console
from rich.prompt import Prompt
import humanize
from alive_progress import alive_bar, config_handler
from loguru import logger
import importlib.util
import sys
from pathlib import Path

def load_config():
    """动态加载配置文件"""
    try:
        # 获取程序运行目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的可执行文件
            app_path = Path(sys.executable).parent
        else:
            # 如果是开发环境
            app_path = Path(__file__).parent

        config_path = app_path / "config.py"

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        # 动态加载配置文件
        spec = importlib.util.spec_from_file_location("config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        # 验证必要的配置项
        required_attrs = ['name', 'username', 'userid', 'themeid', 'items', 'item_info']
        for attr in required_attrs:
            if not hasattr(config_module, attr):
                raise AttributeError(f"配置文件缺少必要的配置项: {attr}")

        return config_module

    except Exception as e:
        logger.error(f"加载配置文件失败: {str(e)}")
        console.print(f"[red]错误: 加载配置文件失败 - {str(e)}[/red]")
        sys.exit(1)

config = load_config()


# 配置 alive-progress 样式
config_handler.set_global(
    spinner='dots_waves',
    bar='classic2',
    title_length=40,
    length=40,
)

console = Console()

# 获取程序运行目录
def get_app_dir():
    """获取应用程序运行目录"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).parent

# 设置路径
APP_DIR = get_app_dir()
REPORTS_DIR = APP_DIR / "reports"
LOGS_DIR = APP_DIR / "logs"

# 确保日志目录存在
LOGS_DIR.mkdir(exist_ok=True)

# 验证 reports 目录
if not REPORTS_DIR.exists():
    logger.error(f"Reports目录不存在: {REPORTS_DIR}")
    raise FileNotFoundError(f"请确保reports目录在程序同级目录下")



# 配置日志
def setup_logging():
    # 清除默认的 logger
    logger.remove()

    # 添加控制台输出
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # 添加文件输出
    log_file = LOGS_DIR / f"experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger.add(
        log_file,
        rotation="500 MB",  # 日志文件大小超过500MB时轮转
        retention="10 days",  # 保留10天的日志
        compression="zip",  # 压缩旧的日志文件
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"  # 文件记录更详细的日志级别
    )


def print_menu():
    console.print("\n[bold cyan]可用实验列表:[/bold cyan]")
    index = 1
    menu_map = {}
    for category, experiments in config.items.items():
        console.print(f"\n[yellow]{category}[/yellow]")
        for exp in experiments:
            console.print(f"  {index}. {exp}")
            menu_map[index] = exp
            index += 1
    return menu_map


def get_selected_items(menu_map):
    while True:
        choice = Prompt.ask("\n请输入实验序号(多个用逗号分隔)，输入'all'选择全部，输入'0'退出")
        if choice == '0':
            logger.info("用户选择退出程序")
            exit(0)
        if choice.lower() == 'all':
            logger.info("用户选择了所有实验")
            return list(menu_map.values())
        try:
            selections = [int(x.strip()) for x in choice.split(',')]
            if all(1 <= x <= len(menu_map) for x in selections):
                selected = [menu_map[x] for x in selections]
                logger.info(f"用户选择了实验: {selected}")
                return selected
            else:
                logger.warning(f"用户输入了无效的序号: {selections}")
                console.print("[red]无效的序号，请重新输入[/red]")
        except ValueError as e:
            logger.error(f"输入格式错误: {str(e)}")
            console.print("[red]输入格式错误，请重新输入[/red]")


def start_experiment(item_id):
    logger.info(f"开始实验 ID: {item_id}")
    url = "http://www.obrsim.com/server/start.do"
    params = {
        "itemID": item_id,
        "subID": "0",
        "userAutoid": f"{config.userid},{config.themeid}",
        "autoid": "",
        "key": "BJOBRSOFT"
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        logger.debug(f"发送请求到 {url} 参数: {params}")
        response = requests.post(url, params=params, headers=headers)
        response.raise_for_status()  # 检查响应状态
        logger.info(f"实验启动成功，返回记录ID: {response.text}")
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"启动实验失败: {str(e)}")
        raise


def stop_experiment(record_id, minutes, item_id):
    logger.info(f"停止实验 记录ID: {record_id}, 用时: {minutes}秒")
    url = "http://www.obrsim.com/server/stop.do"
    params = {
        "studyrecordAutoid": record_id,
        "minutes": str(minutes),
        "score": "1000003",
        "key": "BJOBRSOFT"
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue"
    }

    try:
        report_path = REPORTS_DIR / f"{item_id}.xml"
        logger.debug(f"读取报告文件: {report_path}")
        with open(report_path, 'r', encoding='GB2312') as f:
            report_content = f.read()

        report_content = report_content.replace("{name}", config.name)
        report_content = report_content.replace("{username}", config.username)
        report_content = report_content.replace("{run_time}", str(minutes))
        data = {
            "report": urllib.parse.unquote(report_content)
        }

        logger.debug(f"发送请求到 {url} 参数: {params}")
        response = requests.post(url, params=params, headers=headers, data=data)
        response.raise_for_status()
        logger.info(f"实验停止成功，服务器响应: {response.text}")
        return response.text
    except (IOError, requests.exceptions.RequestException) as e:
        logger.error(f"停止实验失败: {str(e)}")
        raise


def format_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sleep_with_progress(seconds, title):
    """带进度条的休眠函数"""
    with alive_bar(seconds, title=title) as bar:
        for _ in range(seconds):
            time.sleep(1)
            bar()


def main():
    logger.info("程序启动")
    menu_map = print_menu()
    selected_items = get_selected_items(menu_map)

    # 为每个选中的实验添加随机时间
    modified_info = {}
    for item in selected_items:
        info = config.item_info[item].copy()
        info['total_time'] += random.randint(1, 60)
        info['sleep_time'] += random.randint(1, 30)
        modified_info[item] = info
        logger.debug(f"实验 {item} 的修改后时间: total_time={info['total_time']}, sleep_time={info['sleep_time']}")

    # 计算总时间
    total_time = sum(info['total_time'] + info['sleep_time'] for info in modified_info.values())
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=total_time)

    logger.info(f"开始时间: {format_time(start_time)}")
    logger.info(f"预计完成时间: {format_time(end_time)}")
    logger.info(f"预计总用时: {humanize.precisedelta(timedelta(seconds=total_time))}")

    console.print(f"\n[green]开始时间: {format_time(start_time)}[/green]")
    console.print(f"[green]预计完成时间: {format_time(end_time)}[/green]")
    console.print(f"[green]预计总用时: {humanize.precisedelta(timedelta(seconds=total_time))}[/green]\n")

    try:
        for i, item in enumerate(selected_items, 1):
            info = modified_info[item]
            logger.info(f"开始执行第 {i}/{len(selected_items)} 个实验: {item}")

            # 显示当前实验信息
            console.print(f"\n[bold blue]正在进行: {item} ({i}/{len(selected_items)})[/bold blue]")
            next_end_time = datetime.now() + timedelta(seconds=info['total_time'])
            console.print(f"[cyan]当前实验预计完成时间: {format_time(next_end_time)}[/cyan]")

            # 开始实验
            record_id = start_experiment(info['id'])

            # 实验进行（带进度条）
            with alive_bar(info['total_time'], title=f"实验进行中 - {item}", enrich_print=True) as bar:
                for _ in range(info['total_time']):
                    time.sleep(1)
                    bar()

            # 停止实验
            stop_experiment(record_id, info['total_time'], info['id'])

            # 休息时间（带进度条）
            if info['sleep_time'] > 0:
                logger.info(f"休息时间: {info['sleep_time']}秒")
                with alive_bar(info['sleep_time'], title="休息时间", enrich_print=True) as bar:
                    for _ in range(info['sleep_time']):
                        time.sleep(1)
                        bar()

            # 更新剩余时间信息
            if i < len(selected_items):
                remaining_time = sum(
                    (modified_info[rem_item]['total_time'] + modified_info[rem_item]['sleep_time'])
                    for rem_item in selected_items[i:]
                )
                new_end_time = datetime.now() + timedelta(seconds=remaining_time)
                logger.info(f"更新后的预计完成时间: {format_time(new_end_time)}")
                logger.info(f"剩余时间: {humanize.precisedelta(timedelta(seconds=remaining_time))}")

                console.print(f"\n[green]更新后的预计完成时间: {format_time(new_end_time)}[/green]")
                console.print(f"[green]剩余时间: {humanize.precisedelta(timedelta(seconds=remaining_time))}[/green]\n")

    except Exception as e:
        logger.exception("执行实验过程中发生错误")
        console.print(f"\n[bold red]执行过程中发生错误: {str(e)}[/bold red]")
        return

    logger.info("所有实验已成功完成")
    console.print("\n[bold green]所有实验已完成![/bold green]")


if __name__ == "__main__":
    setup_logging()
    main()