# 🌟 cheat-obrsim - 虚拟仿真实验自动化助手 🌟 

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

## 目录

- [项目介绍](#项目介绍)
  - [✨主要特性](#✨主要特性)
  - [🎯核心功能](#🎯核心功能)
  - [⚡使用警告](#⚡使用警告)
  - [🎨技术栈](#🎨技术栈)
  - [💫注意事项](#💫注意事项)
  - [🎭免责声明](#🎭免责声明)
  - [🌈最后的话](#🌈最后的话)
  - [⚠️警告](#⚠️警告)
- [上手指南](#上手指南)
  - [安装步骤](#安装步骤)

### 项目介绍

这是一个神奇的项目，它能让你在虚拟实验室里跳跃，就像量子纠缠一样神秘莫测！

#### ✨主要特性

- 让金刚石在数字世界里跳舞
- 用进度条编织时空隧道
- 把实验报告变成会唱歌的XML精灵
- 让休息时间比相对论还相对

#### 🎯核心功能

* 把时间揉成橡皮泥，随机添加1-60秒的量子涨落
* 让进度条像蠕虫一样爬行，展示平行宇宙中的实验进度
* 把实验数据包装成会飞的数据包，让服务器以为你真的在认真做实验

#### ⚡使用警告

- 请不要在满月时运行程序，可能会召唤出bug精灵
- 休息时间可能会进入第五维度
- 不要尝试理解代码逻辑，这是潘多拉魔盒
- 进度条有时会思考人生，请给它一点时间

#### 🎨技术栈

* Python：因为它像蟒蛇一样神秘
* Rich：让控制台像迪斯科舞厅一样闪烁
* Alive-Progress：用来安抚焦虑的进度条灵魂
* Requests：在互联网上冲浪的冲浪板
* Humanize：把时间变成人类能理解的胡言乱语

#### 💫注意事项

1. 本程序与现实实验室可能存在11维空间的差异
2. 不要在使用时思考人生，否则进度条会害羞
3. 如果你看到进度条开始倒着走，那是它在思考人生
4. 配置文件是用来迷惑服务器的咒语书

#### 🎭免责声明

- 本程序不对任何时空扭曲负责
- 如果你的实验报告开始唱歌，这是正常现象
- 进度条有自己的想法，请尊重它们
- 随机时间可能会把你带到平行宇宙

#### 🌈最后的话

记住，这不是一个普通的自动化工具，这是一个能让虚拟实验变得像魔法一样的神奇装置！让我们一起在代码的海洋里遨游，在进度条的节奏中翩翩起舞！

#### ⚠️警告

使用本程序可能会上瘾，因为它让无聊的实验变得像在打游戏一样有趣！

### 上手指南

**目前该项目仅适配[理工科学生虚拟仿真实验](https://www.ilab-x.com/details/page?id=12413&isView=true)的金刚石的合成及物理性能测试虚拟仿真实验**

**虽然理论上能实现秒完成实验，但作者并不推荐！！！通过最大程度的模仿真实完成的记录，项目运行总时长大约为1-2小时**
**！！！请先使用官方的仿真软件启动，测试成绩是否正常回传**

###### **安装步骤**

1. 克隆仓库或独自下载仓库源代码

```sh
git clone https://github.com/ztearroo/cheat-obrsim.git
```

2. 进入到如图页面，`F12`打开开发者工具并刷新页面

![](/img/img1.png)



3. 如图所示打开搜索，或使用快捷键`ctrl+shift+F`打开

![](/img/img2.png)

4. 搜索`//当前登录用户id`，点开第一条，复制`themeid`、`userid`和`name`到`config.py`当中

![](/img/img3.png)

5. 点击网页右上角进入个人中心，将用户名复制到`config.py`中的`username`当中

![](/img/img5.png)

![](/img/img4.png)

![](/img/img6.png)

6. `config.py`配置完成后，用python运行可`pip install -r requirements.txt` 并在`cmd`中通过`python main.py`运行)

```cmd
cd <项目根目录>

# 安装太慢可用清华源加速
pip install -r requirements.txt

python main.py
```



### 版权说明

该项目签署了MIT 授权许可，详情请参阅 [LICENSE.txt](https://github.com/ztearroo/cheat-obrsim/blob/master/LICENSE.txt)


<!-- links -->
[your-project-path]:ztearroo/cheat-obrsim
[contributors-shield]: https://img.shields.io/github/contributors/ztearroo/cheat-obrsim.svg?style=flat-square
[contributors-url]: https://github.com/ztearroo/cheat-obrsim/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ztearroo/cheat-obrsim.svg?style=flat-square
[forks-url]: https://github.com/ztearroo/cheat-obrsim/network/members
[stars-shield]: https://img.shields.io/github/stars/ztearroo/cheat-obrsim.svg?style=flat-square
[stars-url]: https://github.com/ztearroo/cheat-obrsim/stargazers
[issues-shield]: https://img.shields.io/github/issues/ztearroo/cheat-obrsim.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/ztearroo/cheat-obrsim.svg
[license-shield]: https://img.shields.io/github/license/ztearroo/cheat-obrsim.svg?style=flat-square
[license-url]: https://github.com/ztearroo/cheat-obrsim/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/shaojintian