<div align="center">
  <img src="https://raw.githubusercontent.com/CharlesPikachu/videodl/master/docs/logo.png" width="600"/>
</div>
<br />

<div align="center">
  <a href="https://videofetch.readthedocs.io/">
    <img src="https://img.shields.io/badge/docs-latest-blue" alt="docs" />
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://img.shields.io/pypi/pyversions/videofetch" alt="PyPI - Python Version" />
  </a>
  <a href="https://pypi.org/project/videofetch">
    <img src="https://img.shields.io/pypi/v/videofetch" alt="PyPI" />
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/CharlesPikachu/videodl.svg" alt="license" />
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://static.pepy.tech/badge/videofetch" alt="PyPI - Downloads">
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://static.pepy.tech/badge/videofetch/month" alt="PyPI - Downloads">
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/issues">
    <img src="https://isitmaintained.com/badge/resolution/CharlesPikachu/videodl.svg" alt="issue resolution" />
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/issues">
    <img src="https://isitmaintained.com/badge/open/CharlesPikachu/videodl.svg" alt="open issues" />
  </a>
</div>

<p align="center">
  📄 <strong><a href="https://videofetch.readthedocs.io/" target="_blank">Documents: videofetch.readthedocs.io</a></strong>
</p>


# 🆕 What's New

- 2025-11-21: Released videofetch v0.2.0 - code refactored and extensive support added for downloading videos from many additional platforms.


# 🚀 Introduction

A fast and lightweight video downloader built entirely in Python! 🚀 
If you find this project useful, don't forget to star the repository and help us grow—your support means the world! 🙌


# 📜 Statement

This repository is created solely for learning purposes (commercial use is prohibited). 
All APIs used here are sourced from public networks. 
If you wish to download paid videos, please ensure you have a paid membership on the respective video platform (respect copyright, please!). 
If any content in this repository causes concerns or infringes on copyright, please reach out to me, and I’ll promptly remove it.


# 🎥 Supported Video Client

The video platforms currently supported for parsing are,

| VideoClient (EN)                      |  VideoClient (CN)            | WeChat Article                                              | Search   |  ParseURL  |  Download  | Core Code                                                                                                              |
| :----:                                |  :----:                      | :----:                                                      | :----:   |  :----:    |  :----:    | :----:                                                                                                                 |
| AcFunVideoClient                      |  A站                         | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw)  | ❌       |  ✔️        |  ✔️        | [acfun.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/acfun.py)                     |
| PipigaoxiaoVideoClient                |  皮皮搞笑                    | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [pipigaoxiao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipigaoxiao.py)         |
| PipixVideoClient                      |  皮皮虾                      | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [pipix.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipix.py)                     |
| HaokanVideoClient                     |  好看视频                    | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw)  | ❌       |  ✔️        |  ✔️        | [haokan.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/haokan.py)                   |
| TedVideoClient                        |  TED视频 (演讲视频)          | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [ted.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ted.py)                         |
| Ku6VideoClient                        |  酷6网                       | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [ku6.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ku6.py)                         |
| BilibiliVideoClient                   |  哔哩哔哩 (B站)              | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA)  | ❌       |  ✔️        |  ✔️        | [bilibili.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/bilibili.py)               |
| KuaishouVideoClient                   |  快手                        | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [kuaishou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kuaishou.py)               |
| YinyuetaiVideoClient                  |  音悦台 (官网倒闭ing😭)      | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [yinyuetai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/yinyuetai.py)             |
| BaiduTiebaVideoClient                 |  百度贴吧                    | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [baidutieba.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/baidutieba.py)           |
| MGTVVideoClient                       |  芒果TV                      | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw)  | ❌       |  ✔️        |  ✔️        | [mgtv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/mgtv.py)                       |
| OasisVideoClient                      |  新浪绿洲                    | -                                                           | ❌       |  ✔️        |  ✔️        | [oasis.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/oasis.py)                     |
| PearVideoClient                       |  梨视频                      | -                                                           | ❌       |  ✔️        |  ✔️        | [pear.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pear.py)                       |
| HuyaVideoClient                       |  虎牙视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [huya.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/huya.py)                       |
| DuxiaoshiVideoClient                  |  度小视 (全民小视频)         | -                                                           | ❌       |  ✔️        |  ✔️        | [duxiaoshi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/duxiaoshi.py)             |
| MeipaiVideoClient                     |  美拍                        | -                                                           | ❌       |  ✔️        |  ✔️        | [meipai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/meipai.py)                   |
| SixRoomVideoClient                    |  六间房视频                  | -                                                           | ❌       |  ✔️        |  ✔️        | [sixroom.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sixroom.py)                 |
| WeishiVideoClient                     |  微视                        | -                                                           | ❌       |  ✔️        |  ✔️        | [weishi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/weishi.py)                   |
| ZuiyouVideoClient                     |  最右                        | -                                                           | ❌       |  ✔️        |  ✔️        | [zuiyou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zuiyou.py)                   |
| XinpianchangVideoClient               |  新片场                      | -                                                           | ❌       |  ✔️        |  ✔️        | [xinpianchang.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xinpianchang.py)       |
| WeSingVideoClient                     |  全民K歌                     | -                                                           | ❌       |  ✔️        |  ✔️        | [wesing.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wesing.py)                   |
| XiguaVideoClient                      |  西瓜视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [xigua.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xigua.py)                     |
| RednoteVideoClient                    |  小红书                      | -                                                           | ❌       |  ✔️        |  ✔️        | [rednote.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/rednote.py)                 |
| WeiboVideoClient                      |  微博视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [weibo.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/weibo.py)                     |
| CCTVVideoClient                       |  央视网                      | -                                                           | ❌       |  ✔️        |  ✔️        | [cctv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/cctv.py)                       |
| SohuVideoClient                       |  搜狐视频                    | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [sohu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sohu.py)                       |
| YouTubeVideoClient                    |  油管视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [youtube.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youtube.py)                 |
| ZhihuVideoClient                      |  知乎视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [zhihu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zhihu.py)                     |
| KakaoVideoClient                      |  KakaoTV (韩国在线视频平台)  | -                                                           | ❌       |  ✔️        |  ✔️        | [zhihu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zhihu.py)                     |


# 📦 Install

You have three installation methods to choose from,

```python
# from pip
pip install videofetch
# from github repo method-1
pip install git+https://github.com/CharlesPikachu/videodl.git@master
# from github repo method-2
git clone https://github.com/CharlesPikachu/videodl.git
cd videodl
python setup.py install
```

Also, some video downloaders depend on [Ffmpeg](https://ffmpeg.org/), 
[CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip), [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI), and [Node.js](https://nodejs.org/en),
so please make sure both programs are installed and can be invoked directly from your system environment (*i.e.*, they are on your `PATH`). 
A quick way to verify this is:

- **For Ffmpeg**: open a terminal (or Command Prompt on Windows) and run,
  ```bash
  ffmpeg -version
  ```
  If the installation is correct, you should see detailed version information instead of a "command not found" or "'ffmpeg' is not recognized" error.

- **For CBox and N_m3u8DL-CLI (Windows only for CCTVVideoClient)**:
  You only need to download [CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) from the GitHub releases and add the path to cbox to your environment variables.
  If you don’t need to download the highest-quality videos from CCTV, you don’t need to install this library.
  If your downloader calls it from the command line, you should also be able to run
  ```bash
  python -c "import shutil; print(shutil.which('cbox'))"
  python -c "import shutil; print(shutil.which('N_m3u8DL-CLI'))"
  ```
  in Command Prompt and get the full path without an error.
  If the N_m3u8DL-CLI version is not compatible with your system, please download the appropriate one from the [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI) official website yourself.

- **For Node.js**: open a terminal (or Command Prompt on Windows) and run,
  ```bash
  node -v
  npm -v
  ```
  If Node.js is installed correctly, `node -v` will print the Node.js version (*e.g.*, `v22.11.0`), and `npm -v` will print the npm version.
  If you see a similar `command not found` / `not recognized` error, Node.js is not installed correctly or not available on your `PATH`.


# ⚡ Quick Start

After a successful installation, you can run the snippet below,

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_client.startparseurlcmdui()
```

The demonstration is as follows,

<div align="center">
  <img src="https://github.com/CharlesPikachu/videodl/raw/master/docs/screenshot.gif" width="600"/>
</div>
<br />


# 💡 Recommended Projects

- [Games](https://github.com/CharlesPikachu/Games): Create interesting games in pure python.
- [DecryptLogin](https://github.com/CharlesPikachu/DecryptLogin): APIs for loginning some websites by using requests.
- [Musicdl](https://github.com/CharlesPikachu/musicdl): A lightweight music downloader written in pure python.
- [Videodl](https://github.com/CharlesPikachu/videodl): A lightweight video downloader written in pure python.
- [Pytools](https://github.com/CharlesPikachu/pytools): Some useful tools written in pure python.
- [PikachuWeChat](https://github.com/CharlesPikachu/pikachuwechat): Play WeChat with itchat-uos.
- [Pydrawing](https://github.com/CharlesPikachu/pydrawing): Beautify your image or video.
- [ImageCompressor](https://github.com/CharlesPikachu/imagecompressor): Image compressors written in pure python.
- [FreeProxy](https://github.com/CharlesPikachu/freeproxy): Collecting free proxies from internet.
- [Paperdl](https://github.com/CharlesPikachu/paperdl): Search and download paper from specific websites.
- [Sciogovterminal](https://github.com/CharlesPikachu/sciogovterminal): Browse "The State Council Information Office of the People's Republic of China" in the terminal.
- [CodeFree](https://github.com/CharlesPikachu/codefree): Make no code a reality.
- [DeepLearningToys](https://github.com/CharlesPikachu/deeplearningtoys): Some deep learning toys implemented in pytorch.
- [DataAnalysis](https://github.com/CharlesPikachu/dataanalysis): Some data analysis projects in charles_pikachu.
- [Imagedl](https://github.com/CharlesPikachu/imagedl): Search and download images from specific websites.
- [Pytoydl](https://github.com/CharlesPikachu/pytoydl): A toy deep learning framework built upon numpy.
- [NovelDL](https://github.com/CharlesPikachu/noveldl): Search and download novels from some specific websites.


# 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CharlesPikachu/videodl&type=date&legend=top-left)](https://www.star-history.com/#CharlesPikachu/videodl&type=date&legend=top-left)


# ☕ Appreciation (赞赏 / 打赏)

| WeChat Appreciation QR Code (微信赞赏码)                                                                                       | Alipay Appreciation QR Code (支付宝赞赏码)                                                                                     |
| :--------:                                                                                                                     | :----------:                                                                                                                   |
| <img src="https://raw.githubusercontent.com/CharlesPikachu/videodl/master/.github/pictures/wechat_reward.jpg" width="260" />   | <img src="https://raw.githubusercontent.com/CharlesPikachu/videodl/master/.github/pictures/alipay_reward.png" width="260" />   |


# 📱 WeChat Official Account (微信公众号):

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/videodl/master/docs/pikachu.jpg)