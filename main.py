# main.py
import config
import requests
import urllib.parse
import time
from datetime import datetime, timedelta
import random
from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path
import humanize
from alive_progress import alive_bar, config_handler

# 配置 alive-progress 样式
config_handler.set_global(
    spinner='dots_waves',  # 动画样式
    bar='classic2',  # 进度条样式
    title_length=40,
    length=40,
)

console = Console()

# 获取reports文件夹的绝对路径
SCRIPT_DIR = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "reports"


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
            exit(0)
        if choice.lower() == 'all':
            return list(menu_map.values())
        try:
            selections = [int(x.strip()) for x in choice.split(',')]
            if all(1 <= x <= len(menu_map) for x in selections):
                return [menu_map[x] for x in selections]
            else:
                console.print("[red]无效的序号，请重新输入[/red]")
        except:
            console.print("[red]输入格式错误，请重新输入[/red]")


def start_experiment(item_id):
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
    response = requests.post(url, params=params, headers=headers)
    return response.text


def stop_experiment(record_id, minutes, item_id):
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

    report_path = REPORTS_DIR / f"{item_id}.xml"
    with open(report_path, 'r', encoding='GB2312') as f:
        report_content = f.read()

    report_content = report_content.replace("<name>", config.name)
    report_content = report_content.replace("<username>", config.username)

    data = {
        "report": urllib.parse.unquote(report_content)
    }

    response = requests.post(url, params=params, headers=headers, data=data)
    return response.text


def format_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def sleep_with_progress(seconds, title):
    """带进度条的休眠函数"""
    with alive_bar(seconds, title=title) as bar:
        for _ in range(seconds):
            time.sleep(1)
            bar()


def main():
    menu_map = print_menu()
    selected_items = get_selected_items(menu_map)

    # 为每个选中的实验添加随机时间
    modified_info = {}
    for item in selected_items:
        info = config.item_info[item].copy()
        info['total_time'] += random.randint(1, 60)
        info['sleep_time'] += random.randint(1, 30)
        modified_info[item] = info

    # 计算总时间
    total_time = sum(info['total_time'] + info['sleep_time'] for info in modified_info.values())
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=total_time)

    console.print(f"\n[green]开始时间: {format_time(start_time)}[/green]")
    console.print(f"[green]预计完成时间: {format_time(end_time)}[/green]")
    console.print(f"[green]预计总用时: {humanize.precisedelta(timedelta(seconds=total_time))}[/green]\n")

    for i, item in enumerate(selected_items, 1):
        info = modified_info[item]

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
        stop_experiment(record_id, info['total_time'] // 60, info['id'])

        # 休息时间（带进度条）
        if info['sleep_time'] > 0:
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
            console.print(f"\n[green]更新后的预计完成时间: {format_time(new_end_time)}[/green]")
            console.print(f"[green]剩余时间: {humanize.precisedelta(timedelta(seconds=remaining_time))}[/green]\n")

    console.print("\n[bold green]所有实验已完成![/bold green]")


if __name__ == "__main__":
    main()