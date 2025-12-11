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

<p align="center">
  🌌 <strong><a href="https://charlespikachu.github.io/videodl/" target="_blank">VideoDL Live Status Dashboard (VideoDL有效性实时监测)</a></strong><br/>
  <sub>Auto-updated every day via GitHub Actions, with ~3 randomly sampled preview clips.</sub><br/><br/>
  <a href="https://charlespikachu.github.io/videodl/">
    <img
      alt="demo"
      src="https://img.shields.io/badge/demo-online-brightgreen?style=for-the-badge"
    />
  </a>
</p>


# 🆕 What's New

- 2025-12-12: Released videofetch v0.3.5 - added support for parsing on two specific platforms and introduced a generic parsing interface.
- 2025-12-11: Released videofetch v0.3.4 - fix the problems with downloading CCTV videos.
- 2025-12-08: Released videofetch v0.3.3 - some simple code fixes, and a generic xiami parsing interface has been added.
- 2025-12-06: Released videofetch v0.3.2 - added a new generic parsing interface, support for parsing two specific websites, and special handling of Base64 encoding in parts of the generic parser.
- 2025-12-06: Released videofetch v0.3.1 - added several general-purpose parsers and made some minor feature improvements.
- 2025-12-05: Released videofetch v0.3.0 - add support for more sites and introduce features of the generic parser to help enable parsing across the entire web.
- 2025-11-29: Released videofetch v0.2.3 - add support for `FoxNewsVideoClient` and `SinaVideoClient`, and introduce N_m3u8DL-RE to improve the download speed of HLS/m3u8 streams.


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
| TedVideoClient                        |  TED视频                     | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [ted.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ted.py)                         |
| Ku6VideoClient                        |  酷6网                       | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [ku6.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ku6.py)                         |
| BilibiliVideoClient                   |  哔哩哔哩 (B站)              | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA)  | ❌       |  ✔️        |  ✔️        | [bilibili.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/bilibili.py)               |
| KuaishouVideoClient                   |  快手                        | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [kuaishou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kuaishou.py)               |
| YinyuetaiVideoClient                  |  音悦台 (关停ing😭)          | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [yinyuetai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/yinyuetai.py)             |
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
| KakaoVideoClient                      |  KakaoTV                     | -                                                           | ❌       |  ✔️        |  ✔️        | [kakao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kakao.py)                     |
| YoukuVideoClient                      |  优酷视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [youku.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youku.py)                     |
| TencentVideoClient                    |  腾讯视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [tencent.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/tencent.py)                 |
| GeniusVideoClient                     |  Rap Genius (嘻哈百科)       | -                                                           | ❌       |  ✔️        |  ✔️        | [genius.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/genius.py)                   |
| UnityVideoClient                      |  Unity                       | -                                                           | ❌       |  ✔️        |  ✔️        | [unity.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/unity.py)                     |
| FoxNewsVideoClient                    |  福克斯新闻                  | -                                                           | ❌       |  ✔️        |  ✔️        | [foxnews.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/foxnews.py)                 |
| SinaVideoClient                       |  新浪视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [sina.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sina.py)                       |
| XuexiCNVideoClient                    |  学习强国                    | -                                                           | ❌       |  ✔️        |  ✔️        | [xuexicn.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xuexicn.py)                 |
| Open163VideoClient                    |  网易公开课                  | -                                                           | ❌       |  ✔️        |  ✔️        | [open163.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/open163.py)                 |
| CCtalkVideoClient                     |  CCtalk                      | -                                                           | ❌       |  ✔️        |  ✔️        | [cctalk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/cctalk.py)                   |
| EyepetizerVideoClient                 |  开眼视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [eyepetizer.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/eyepetizer.py)           |
| ArteTVVideoClient                     |  德法公共电视网              | -                                                           | ❌       |  ✔️        |  ✔️        | [artetv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/artetv.py)                   |
| C56VideoClient                        |  56视频网                    | -                                                           | ❌       |  ✔️        |  ✔️        | [c56.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/c56.py)                         |
| RedditVideoClient                     |  红迪网                      | -                                                           | ❌       |  ✔️        |  ✔️        | [reddit.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/reddit.py)                   |

To make videodl more robust and able to adaptively parse videos from more websites, even when the video URL is not in the supported list above, 
I also plan to gradually add some general-purpose parsing interfaces. The currently supported generic parsers include:

| CommonVideoClient (EN)                                          |  CommonVideoClient (CN)                                    | ParseURL  |  Download  | Core Code                                                                                                              |
| :----:                                                          |  :----:                                                    | :----:    |  :----:    | :----:                                                                                                                 |
| [IIILabVideoClient](https://roar.iiilab.com/)                   |  [兽音译者](https://roar.iiilab.com/)                      | ✔️        |  ✔️        | [iiilab.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/iiilab.py)                    |
| [KedouVideoClient](https://www.kedou.life/)                     |  [Kedou视频解析](https://www.kedou.life/)                  | ✔️        |  ✔️        | [kedou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/kedou.py)                      |
| [SnapAnyVideoClient](https://snapany.com/zh)                    |  [SnapAny万能解析](https://snapany.com/zh)                 | ✔️        |  ✔️        | [snapany.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/snapany.py)                  |
| [GVVIPVideoClient](https://greenvideo.cc/video/vip)             |  [GreenVideoVIP视频解析](https://greenvideo.cc/video/vip)  | ✔️        |  ✔️        | [gvvip.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/gvvip.py)                      |
| [VgetVideoClient](https://vget.xyz/)                            |  [Vget视频解析](https://vget.xyz/)                         | ✔️        |  ✔️        | [vget.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/vget.py)                        |
| [ILoveAPIVideoClient](https://www.52api.cn/)                    |  [我爱API](https://www.52api.cn/)                          | ✔️        |  ✔️        | [iloveapi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/iloveapi.py)                |
| [XMFlvVideoClient](https://jx.xmflv.com/)                       |  [虾米解析](https://jx.xmflv.com/)                         | ✔️        |  ✔️        | [xmflv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xmflv.py)                      |
| [QZXDPToolsVideoClient](https://tools.qzxdp.cn/video_spider)    |  [全栈工具视频解析](https://tools.qzxdp.cn/video_spider)   | ✔️        |  ✔️        | [qzxdptools.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/qzxdptools.py)            |

The default parsing order is to first use the parsers in the supported list. If those fail, the generic parsers are then invoked one by one until parsing succeeds.


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

Some of the video downloaders supported by `videodl` rely on additional CLI tools to enable video decryption, stream parsing and downloading, accelerated stream downloading, and other extended features such as resuming interrupted downloads. 
Specifically, these CLI tools include,

- **[FFmpeg](https://ffmpeg.org/)**: All video downloaders that need to handle HLS (HTTP Live Streaming) streams depend on FFmpeg. Therefore, we recommend that all `videodl` users install FFmpeg.
  Specifically, you need to ensure that, after installation, FFmpeg can be invoked directly from your system environment (*i.e.*, it is on your `PATH`).
  A quick way to verify this is to open a terminal (or Command Prompt on Windows) and run,
  ```bash
  ffmpeg -version
  ```
  If the installation is correct, you should see detailed version information instead of a "command not found" or "'ffmpeg' is not recognized" error.
  
- **[CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) and [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI)**: 
  These two CLI tools are only used to fix the issue of corrupted (garbled) video when downloading HD videos with `CCTVVideoClient` due to encrypted m3u8 links. 
  You only need to download [CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) from the GitHub releases and add the path to cbox to your environment variables.
  If you don’t need to use `CCTVVideoClient` to download HD videos, you don’t need to configure these two CLI tools.
  As with FFmpeg, after installation you should make sure these tools can be run directly from the command line, *i.e.*, their location is included in your system `PATH`.
  A quick way to verify this is that you should be able to run
  ```bash
  python -c "import shutil; print(shutil.which('cbox'))"
  python -c "import shutil; print(shutil.which('N_m3u8DL-CLI'))"
  ```
  in Command Prompt and get the full path without an error.
  If the N_m3u8DL-CLI version is not compatible with your system, please download the appropriate one from the [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI) official website yourself.

- **[Node.js](https://nodejs.org/en)**: Currently, Node.js is only used in `YouTubeVideoClient` to execute certain JavaScript code for video parsing. 
  Therefore, if you don’t need to use `YouTubeVideoClient`, you can safely skip installing this CLI tool.
  A quick way to check whether Node.js has been installed successfully is to open a terminal (or Command Prompt on Windows) and run:
  ```bash
  node -v (npm -v)
  ```
  If Node.js is installed correctly, `node -v` will print the Node.js version (*e.g.*, `v22.11.0`), and `npm -v` will print the npm version.
  If you see a similar `command not found` / `not recognized` error, Node.js is not installed correctly or not available on your `PATH`.

- **[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)**: 
  FFmpeg is a general-purpose media tool that can download standard HLS/m3u8 streams, but it assumes that the playlist and segment URLs strictly follow the protocol. 
  N_m3u8DL-RE is a specialized m3u8 downloader that adds extensive logic for handling encryption, anti-leech headers, redirects, and malformed playlists, so it can capture many ‘protected’ or non-standard videos that FFmpeg fails on. 
  Therefore, for some sites where downloading m3u8 streams with FFmpeg is throttled or fails, we recommend installing and using N_m3u8DL-RE instead.
  Currently, the video downloaders that use N_m3u8DL-RE by default include `FoxNewsVideoClient`, `TencentVideoClient`, `GVVIPVideoClient`, `SnapAnyVideoClient`, `VgetVideoClient`, `ArteTVVideoClient`, `XMFlvVideoClient`, `RedditVideoClient` and `IIILabVideoClient`. 
  Therefore, if you don’t need to download videos from these two platforms, you can choose not to install this CLI tool.
  As with FFmpeg, after installation you should make sure this tool can be run directly from the command line, *i.e.*, its location is included in your system `PATH`.
  A quick way to check whether N_m3u8DL-RE has been installed successfully is to open a terminal (or Command Prompt on Windows) and run:
  ```bash
  N_m3u8DL-RE --version
  ```
  If N_m3u8DL-RE is installed correctly, `N_m3u8DL-RE --version` will print the N_m3u8DL-RE version (*e.g.*, `0.5.1+c1f6db5639397dde362c31b31eebd88c796c90da`).
  If you see a similar `command not found` / `not recognized` error, N_m3u8DL-RE is not installed correctly or not available on your `PATH`.

- **[aria2c](https://aria2.github.io/)**: `videodl` now also supports manually integrating aria2c to accelerate downloads (for example, MP4 files) and to enable resuming interrupted video downloads, *etc*. 
  Before using this feature, you must ensure that aria2c is available on the system `PATH` in your runtime environment. 
  You can verify this by opening a terminal and running `aria2c --version` (or `aria2c -v`); if the command returns version information instead of a `“command not found”` error, 
  then aria2c is correctly installed and detectable. On Linux/macOS you can also run `which aria2c`, and on Windows `where aria2c`, to confirm that the executable can be found.
  To enable aria2c during video downloading, please refer to the [Quick Start](https://github.com/CharlesPikachu/videodl?tab=readme-ov-file#-quick-start) section.


# ⚡ Quick Start

After a successful installation, you can run the snippet below,

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_client.startparseurlcmdui()
```

Or just run `videodl -i "URL"` (maybe `videodl --help` to show usage information) from the terminal.

```bash
Usage: videodl [OPTIONS]

Options:
  --version                       Show the version and exit.
  -i, --index-url, --index_url TEXT
                                  URL of the video to download. If not
                                  specified, videodl will start in terminal
                                  mode.
  -a, --allowed-video-sources, --allowed_video_sources TEXT
                                  Platforms to search. Separate multiple
                                  platforms with "," (e.g.,
                                  "AcFunVideoClient,PipixVideoClient"). If not
                                  specified, videodl will search all supported
                                  platforms globally and use the first one
                                  that can download the video url.
  -c, --init-video-clients-cfg, --init_video_clients_cfg TEXT
                                  Config such as `work_dir` for each video
                                  client as a JSON string.
  -r, --requests-overrides, --requests_overrides TEXT
                                  Requests.get kwargs such as `headers` and
                                  `proxies` for each video client as a JSON
                                  string.
  -t, --clients-threadings, --clients_threadings TEXT
                                  Number of threads used for each video client
                                  as a JSON string.
  -g, --apply-common-video-clients-only, --apply_common_video_clients_only
                                  Only apply common video clients.
  --help                          Show this message and exit.
```

The demonstration is as follows,

<div align="center">
  <img src="https://github.com/CharlesPikachu/videodl/raw/master/docs/screenshot.gif" width="600"/>
</div>
<br />

If you just want to parse a video link and retrieve information about the video, you can do it like this,

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://v.youku.com/v_show/id_XNDUxOTc1NDg4MA==.html?spm=a2hkl.14919748_WEBHOME_HOME.scg_scroll_3.d_2_play&s=faab858435f24d5bb6d3&scm=20140719.rcmd.feed.show_faab858435f24d5bb6d3&alginfo=-1reqId-249a939e8%203783%204341%2099d9%20974d2b07ad23%231764142230027-1seqId-20IX2riz0CjZG971l-1abId-2468080-1sceneId-246595&scg_id=22896555")
print(video_infos)
```

The output of this code looks like,

```python
[
  {
    "source": "YoukuVideoClient",
    "raw_data": {
      "cost": 0.020000001,
      ...
    },
    "download_url": "http://pl-ali.youku.com/playlist/m3u8?vid=XNDUxOTc1NDg4MA%3D%3D&type=mp4hd2v3&ups_client_netip=725c13f7&utid=dJytIY%2Bx4WYCAXJcE%2Few6YTM&ccode=0564&psid=2fb1945e5c8cc1b213f831c70ace818841346&duration=2205&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1764142708&onOff=0&encr=0&ups_key=f30ad69f9025369053e0932bfe1d2276&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0",
    "title": "史家绝唱",
    "file_path": "videodl_outputs\\YoukuVideoClient\\史家绝唱.m3u",
    "ext": "m3u",
    "download_with_ffmpeg": true,
    "err_msg": "NULL",
    "identifier": "XNDUxOTc1NDg4MA==",
    "guess_video_ext_result": {
      "ext": "m3u",
      "sniffer": "requests.head",
      "ok": true
    }
  }
]
```

Then you can also call the video downloading function to download the video parsed by videodl. The code is as follows:

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://v.youku.com/v_show/id_XNDUxOTc1NDg4MA==.html?spm=a2hkl.14919748_WEBHOME_HOME.scg_scroll_3.d_2_play&s=faab858435f24d5bb6d3&scm=20140719.rcmd.feed.show_faab858435f24d5bb6d3&alginfo=-1reqId-249a939e8%203783%204341%2099d9%20974d2b07ad23%231764142230027-1seqId-20IX2riz0CjZG971l-1abId-2468080-1sceneId-246595&scg_id=22896555")
video_client.download(video_infos=video_infos)
```

If you want to use aria2c to accelerate the download of non-HLS/m3u8 streams, such as mp4 files, you can do the following:

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://www.bilibili.com/video/BV1KZgHzJEs6/?spm_id_from=333.337.search-card.all.click")
for v in video_infos: v['download_with_aria2c'] = True
video_client.download(video_infos=video_infos)
```

If you want to use N_m3u8DL-RE to speed up the download of HLS/m3u8 streams, you can do the following:

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://www.acfun.cn/v/ac36491489")
for v in video_infos: v['enable_nm3u8dlre'] = True
video_client.download(video_infos=video_infos)
```

If you know that the video you want to parse is definitely not in the supported list and you want to use the generic parser directly, you can set `apply_common_video_clients_only` to `True`, *e.g.*,
just run `videodl -i "URL" -g` from the terminal, or coding as following,

```python
from videodl import videodl

video_client = videodl.VideoClient(apply_common_video_clients_only=True)
video_client.startparseurlcmdui()
```

If you’re a VIP member of a video platform, such as Tencent Video, you can try the following code to improve the quality of the videos you download:

```python
from videodl import videodl

your_vip_cookies_with_str_or_dict_format = ""
init_video_clients_cfg = dict()
init_video_clients_cfg['TencentVideoClient'] = {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format, 'default_download_cookies': your_vip_cookies_with_str_or_dict_format}
video_client = videodl.VideoClient(init_video_clients_cfg=init_video_clients_cfg)
video_client.startparseurlcmdui()
```

Alternatively, you can run the following command directly in the terminal:

```bash
videodl -i "URL" -c "{'TencentVideoClient': {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format, 'default_download_cookies': your_vip_cookies_with_str_or_dict_format}}"
```

If you want to speed up the parsing, you can try specifying the parser used for the video you’re downloading. 
For example, when downloading a Douyin video, you can run the command like this:

```bash
videodl -i "https://www.douyin.com/jingxuan?modal_id=7538145141593263403" -g -a "ILoveAPIVideoClient"
```


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


# 📚 Citation

If you use this project in your research, please cite the repository.

```
@misc{freeproxy2022,
    author = {Zhenchao Jin},
    title = {Videodl: A lightweight video downloader written in pure python},
    year = {2021},
    publisher = {GitHub},
    journal = {GitHub repository},
    howpublished = {\url{https://github.com/CharlesPikachu/videodl/}},
}
```


# 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=CharlesPikachu/videodl&type=date&legend=top-left)](https://www.star-history.com/#CharlesPikachu/videodl&type=date&legend=top-left)


# ☕ Appreciation (赞赏 / 打赏)

| WeChat Appreciation QR Code (微信赞赏码)                                                                                       | Alipay Appreciation QR Code (支付宝赞赏码)                                                                                     |
| :--------:                                                                                                                     | :----------:                                                                                                                   |
| <img src="https://raw.githubusercontent.com/CharlesPikachu/videodl/master/.github/pictures/wechat_reward.jpg" width="260" />   | <img src="https://raw.githubusercontent.com/CharlesPikachu/videodl/master/.github/pictures/alipay_reward.png" width="260" />   |


# 📱 WeChat Official Account (微信公众号):

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/videodl/master/docs/pikachu.jpg)