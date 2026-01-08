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

<p align="center">
  <strong>学习收获更多有趣的内容, 欢迎关注微信公众号：Charles的皮卡丘</strong>
</p>


# 🆕 What's New

- 2026-01-09: Released videofetch v0.5.0 - refactored the code structure, improved the stability of some video clients, removed deprecated interfaces and paid platforms, and fixed some potential bugs.
- 2026-01-01: Released videofetch v0.4.6 - fix a bug when dealing with special download url type.


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

| Category                                               | VideoClient (EN)                      | VideoClient (CN)                   | ParseURL  | Download | Core Code                                                                                                          |
| :--                                                    | :--                                   | :--                                | :--:      | :--:     | :--                                                                                                                |
| **Chinese Platforms**                                  | AcFunVideoClient                      | A站                                | ✔️        | ✔️       | [acfun.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/acfun.py)                 |
|                                                        | BaiduTiebaVideoClient                 | 百度贴吧                           | ✔️        | ✔️       | [baidutieba.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/baidutieba.py)       |
|                                                        | BilibiliVideoClient                   | 哔哩哔哩 (B站)                     | ✔️        | ✔️       | [bilibili.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/bilibili.py)           |
|                                                        | C56VideoClient                        | 56视频网                           | ✔️        | ✔️       | [c56.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/c56.py)                     |
|                                                        | CCTVVideoClient                       | 央视网                             | ✔️        | ✔️       | [cctv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/cctv.py)                   |
|                                                        | CCtalkVideoClient                     | CCtalk                             | ✔️        | ✔️       | [cctalk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/cctalk.py)               |
|                                                        | DuxiaoshiVideoClient                  | 度小视 (全民小视频)                | ✔️        | ✔️       | [duxiaoshi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/duxiaoshi.py)         |
|                                                        | EyepetizerVideoClient                 | 开眼视频                           | ✔️        | ✔️       | [eyepetizer.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/eyepetizer.py)       |
|                                                        | HaokanVideoClient                     | 好看视频                           | ✔️        | ✔️       | [haokan.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/haokan.py)               |
|                                                        | HuyaVideoClient                       | 虎牙视频                           | ✔️        | ✔️       | [huya.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/huya.py)                   |
|                                                        | IQiyiVideoClient                      | 爱奇艺                             | ✔️        | ✔️       | [iqiyi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/iqiyi.py)                 |
|                                                        | Ku6VideoClient                        | 酷6网                              | ✔️        | ✔️       | [ku6.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ku6.py)                     |
|                                                        | KuaishouVideoClient                   | 快手                               | ✔️        | ✔️       | [kuaishou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kuaishou.py)           |
|                                                        | MeipaiVideoClient                     | 美拍                               | ✔️        | ✔️       | [meipai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/meipai.py)               |
|                                                        | MGTVVideoClient                       | 芒果TV                             | ✔️        | ✔️       | [mgtv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/mgtv.py)                   |
|                                                        | M1905VideoClient                      | 1905电影网                         | ✔️        | ✔️       | [m1905.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/m1905.py)                 |
|                                                        | OasisVideoClient                      | 新浪绿洲                           | ✔️        | ✔️       | [oasis.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/oasis.py)                 |
|                                                        | Open163VideoClient                    | 网易公开课                         | ✔️        | ✔️       | [open163.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/open163.py)             |
|                                                        | PearVideoClient                       | 梨视频                             | ✔️        | ✔️       | [pear.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pear.py)                   |
|                                                        | PipigaoxiaoVideoClient                | 皮皮搞笑                           | ✔️        | ✔️       | [pipigaoxiao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipigaoxiao.py)     |
|                                                        | PipixVideoClient                      | 皮皮虾                             | ✔️        | ✔️       | [pipix.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipix.py)                 |
|                                                        | RednoteVideoClient                    | 小红书                             | ✔️        | ✔️       | [rednote.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/rednote.py)             |
|                                                        | SinaVideoClient                       | 新浪视频                           | ✔️        | ✔️       | [sina.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sina.py)                   |
|                                                        | SixRoomVideoClient                    | 六间房视频                         | ✔️        | ✔️       | [sixroom.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sixroom.py)             |
|                                                        | SohuVideoClient                       | 搜狐视频                           | ✔️        | ✔️       | [sohu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sohu.py)                   |
|                                                        | TencentVideoClient                    | 腾讯视频                           | ✔️        | ✔️       | [tencent.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/tencent.py)             |
|                                                        | WeiboVideoClient                      | 微博视频                           | ✔️        | ✔️       | [weibo.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/weibo.py)                 |
|                                                        | WeishiVideoClient                     | 微视                               | ✔️        | ✔️       | [weishi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/weishi.py)               |
|                                                        | WeSingVideoClient                     | 全民K歌                            | ✔️        | ✔️       | [wesing.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wesing.py)               |
|                                                        | XiguaVideoClient                      | 西瓜视频                           | ✔️        | ✔️       | [xigua.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xigua.py)                 |
|                                                        | XinpianchangVideoClient               | 新片场                             | ✔️        | ✔️       | [xinpianchang.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xinpianchang.py)   |
|                                                        | XuexiCNVideoClient                    | 学习强国                           | ✔️        | ✔️       | [xuexicn.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xuexicn.py)             |
|                                                        | YoukuVideoClient                      | 优酷视频                           | ✔️        | ✔️       | [youku.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youku.py)                 |
|                                                        | YinyuetaiVideoClient                  | 音悦台 (关停ing😭)                 | ✔️        | ✔️       | [yinyuetai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/yinyuetai.py)         |
|                                                        | ZhihuVideoClient                      | 知乎视频                           | ✔️        | ✔️       | [zhihu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zhihu.py)                 |
|                                                        | ZuiyouVideoClient                     | 最右                               | ✔️        | ✔️       | [zuiyou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zuiyou.py)               |
| **Overseas Platforms**                                 | ArteTVVideoClient                     | 德法公共电视网                     | ✔️        | ✔️       | [artetv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/artetv.py)               |
|                                                        | FoxNewsVideoClient                    | 福克斯新闻                         | ✔️        | ✔️       | [foxnews.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/foxnews.py)             |
|                                                        | GeniusVideoClient                     | Rap Genius (嘻哈百科)              | ✔️        | ✔️       | [genius.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/genius.py)               |
|                                                        | KakaoVideoClient                      | KakaoTV                            | ✔️        | ✔️       | [kakao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kakao.py)                 |
|                                                        | RedditVideoClient                     | 红迪网                             | ✔️        | ✔️       | [reddit.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/reddit.py)               |
|                                                        | TedVideoClient                        | TED视频                            | ✔️        | ✔️       | [ted.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ted.py)                     |
|                                                        | UnityVideoClient                      | Unity                              | ✔️        | ✔️       | [unity.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/unity.py)                 |
|                                                        | WWEVideoClient                        | 世界摔角娱乐                       | ✔️        | ✔️       | [wwe.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wwe.py)                     |
|                                                        | YouTubeVideoClient                    | 油管视频                           | ✔️        | ✔️       | [youtube.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youtube.py)             |

To make videodl more robust and able to adaptively parse videos from more websites, even when the video URL is not in the supported list above, 
I also plan to gradually add some general-purpose parsing interfaces. The currently supported generic parsers include,

| CommonVideoClient (EN)                                            | CommonVideoClient (CN)                                          | ParseURL | Download | Core Code                                                                                                   |
| :--------------------------------------------------------------   | :-------------------------------------------------------------  | :-----:  | :-----:  | :---------------------------------------------------------------------------------------------------------- |
| [BVVideoClient](https://www.bestvideow.com/xhs)                   | [BestVideo下载器](https://www.bestvideow.com/xhs)               |   ✔️     |   ✔️     | [bv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/bv.py)                 |
| [BugPkVideoClient](https://sv.bugpk.com/)                         | [短视频解析工具](https://sv.bugpk.com/)                         |   ✔️     |   ✔️     | [bugpk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/bugpk.py)           |
| [GVVIPVideoClient](https://greenvideo.cc/video/vip)               | [GreenVideoVIP视频解析](https://greenvideo.cc/video/vip)        |   ✔️     |   ✔️     | [gvvip.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/gvvip.py)           |
| [IIILabVideoClient](https://roar.iiilab.com/)                     | [兽音译者](https://roar.iiilab.com/)                            |   ✔️     |   ✔️     | [iiilab.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/iiilab.py)         |
| [KedouVideoClient](https://www.kedou.life/)                       | [Kedou视频解析](https://www.kedou.life/)                        |   ✔️     |   ✔️     | [kedou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/kedou.py)           |
| [KuKuToolVideoClient](https://dy.kukutool.com/)                   | [KuKuTool视频解析](https://dy.kukutool.com/)                    |   ✔️     |   ✔️     | [kukutool.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/kukutool.py)     |
| [LongZhuVideoClient](https://www.hhlqilongzhu.cn/H5_home.php)     | [龙珠API视频解析](https://www.hhlqilongzhu.cn/H5_home.php)      |   ✔️     |   ✔️     | [longzhu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/longzhu.py)       |
| [NoLogoVideoClient](https://nologo.code24.top/)                   | [去水印下载鸭](https://nologo.code24.top/)                      |   ✔️     |   ✔️     | [nologo.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/nologo.py)         |
| [QingtingVideoClient](https://33tool.com/video_parse/)            | [蜻蜓工具](https://33tool.com/video_parse/)                     |   ✔️     |   ✔️     | [qingting.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/qingting.py)     |
| [QZXDPToolsVideoClient](https://tools.qzxdp.cn/video_spider)      | [全栈工具视频解析](https://tools.qzxdp.cn/video_spider)         |   ✔️     |   ✔️     | [qzxdptools.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/qzxdptools.py) |
| [SnapAnyVideoClient](https://snapany.com/zh)                      | [SnapAny万能解析](https://snapany.com/zh)                       |   ✔️     |   ✔️     | [snapany.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/snapany.py)       |
| [SnapWCVideoClient](https://snapwc.com/zh)                        | [SnapWC视频解析](https://snapwc.com/zh)                         |   ✔️     |   ✔️     | [snapwc.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/snapwc.py)         |
| [VgetVideoClient](https://vget.xyz/)                              | [Vget视频解析](https://vget.xyz/)                               |   ✔️     |   ✔️     | [vget.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/vget.py)             |
| [VideoFKVideoClient](https://www.videofk.com/)                    | [免费短视频下载器](https://www.videofk.com/)                    |   ✔️     |   ✔️     | [videofk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/videofk.py)       |
| [XiazaitoolVideoClient](https://www.xiazaitool.com/dy)            | [下载狗](https://www.xiazaitool.com/dy)                         |   ✔️     |   ✔️     | [xiazaitool.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xiazaitool.py) |
| [XMFlvVideoClient](https://jx.xmflv.com/)                         | [虾米解析](https://jx.xmflv.com/)                               |   ✔️     |   ✔️     | [xmflv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xmflv.py)           |
| [ZanqianbaVideoClient](https://www.zanqianba.com/)                | [考拉解析](https://www.zanqianba.com/)                          |   ✔️     |   ✔️     | [zanqianba.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/zanqianba.py)   |

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

Some of the video downloaders supported by videodl rely on additional CLI tools to enable video decryption, stream parsing and downloading, accelerated stream downloading, and other extended features such as resuming interrupted downloads. 
Specifically, these CLI tools include,

- **[FFmpeg](https://ffmpeg.org/)**: All video downloaders that need to handle HLS (HTTP Live Streaming) streams depend on FFmpeg. ❗ **Therefore, we recommend that all videodl users install FFmpeg.** ❗
  Specifically, you need to ensure that, after installation, FFmpeg can be invoked directly from your system environment (*i.e.*, it is on your `PATH`).
  A quick way to verify this is to open a terminal (or Command Prompt on Windows) and run,
  ```bash
  ffmpeg -version
  ```
  If the installation is correct, you should see detailed version information instead of a "command not found" or "'ffmpeg' is not recognized" error.

- **[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)**: 
  FFmpeg is a general-purpose media tool that can download standard HLS/m3u8 streams, but it assumes that the playlist and segment URLs strictly follow the protocol. 
  N_m3u8DL-RE is a specialized m3u8 downloader that adds extensive logic for handling encryption, anti-leech headers, redirects, and malformed playlists, so it can capture many ‘protected’ or non-standard videos that FFmpeg fails on. 
  In many cases it’s also faster, because N_m3u8DL-RE can download HLS segments in parallel with optimized retries/merging, while FFmpeg typically pulls segments sequentially by default.
  ❗ **Therefore, we recommend that all videodl users install N_m3u8DL-RE to ensure videodl delivers the best possible performance.** ❗
  Of course, you can choose not to install it, but in that case you may not be able to use videodl to parse the following platforms,
  ```
  CCTVVideoClient, FoxNewsVideoClient, TencentVideoClient, GVVIPVideoClient, 
  SnapAnyVideoClient, VgetVideoClient, ArteTVVideoClient, XMFlvVideoClient, 
  RedditVideoClient, IIILabVideoClient, WWEVideoClient, IQiyiVideoClient,
  ```
  and downloads from many other sites that provide m3u8/HLS streams may also be significantly limited.
  As with FFmpeg, after installation you should make sure this tool can be run directly from the command line, *i.e.*, its location is included in your system `PATH`.
  A quick way to check whether N_m3u8DL-RE has been installed successfully is to open a terminal (or Command Prompt on Windows) and run,
  ```bash
  N_m3u8DL-RE --version
  ```
  If N_m3u8DL-RE is installed correctly, `N_m3u8DL-RE --version` will print the N_m3u8DL-RE version (*e.g.*, `0.5.1+c1f6db5639397dde362c31b31eebd88c796c90da`).
  If you see a similar `command not found` / `not recognized` error, N_m3u8DL-RE is not installed correctly or not available on your `PATH`.

- **[CBox](https://github.com/CharlesPikachu/videodl/releases/tag/clitools)**:
  CBox is an optional dependency for `CCTVVideoClient`. It helps prevent garbled output when downloading HD streams, which can happen when the m3u8 playlist is encrypted.
  To enable it, download CBox from the GitHub release above and add the CBox folder to your system `PATH`.
  If you intend to use `CCTVVideoClient`, you should also install [FFmpeg](https://ffmpeg.org/) and [N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE) and ensure they are available on your `PATH` as well.
  If you’re not using `CCTVVideoClient` for HD downloads, you can skip the CBox setup entirely.
  To verify your setup, these commands should print the full executable paths (instead of returning nothing),
  ```bash
  python -c "import shutil; print(shutil.which('cbox'))"
  python -c "import shutil; print(shutil.which('N_m3u8DL-RE'))"
  python -c "import shutil; print(shutil.which('ffmpeg'))"
  ```

- **[Node.js](https://nodejs.org/en)**: Currently, Node.js is only used in `YouTubeVideoClient` to execute certain JavaScript code for video parsing. 
  Therefore, if you don’t need to use `YouTubeVideoClient`, you can safely skip installing this CLI tool.
  A quick way to check whether Node.js has been installed successfully is to open a terminal (or Command Prompt on Windows) and run,
  ```bash
  node -v (npm -v)
  ```
  If Node.js is installed correctly, `node -v` will print the Node.js version (*e.g.*, `v22.11.0`), and `npm -v` will print the npm version.
  If you see a similar `command not found` / `not recognized` error, Node.js is not installed correctly or not available on your `PATH`.

- **[aria2c](https://aria2.github.io/)**: videodl now also supports manually integrating aria2c to accelerate downloads (for example, MP4 files) and to enable resuming interrupted video downloads, *etc*. 
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

Recommended parsing and downloading commands for some widely used video platforms are as follows,

```python
# IQIYI / YOUKU / TENCENT (爱奇艺, 优酷, 腾讯视频)
videodl -i "IQIYI/YOUKU/TENCENT VIDEO URL" -g -a XMFlvVideoClient
# MIGU (咪咕视频)
videodl -i "MIGU VIDEO URL" -g -a KedouVideoClient
# DOUYIN / TIKTOK / KUAISHOU / XIAOHONGSHU / YouTubeVideoClient (抖音, 抖音海外, 快手, 小红书, 油管视频等)
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YouTubeVideoClient VIDEO URL" -g -a SnapWCVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YouTubeVideoClient VIDEO URL" -g -a VideoFKVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YouTubeVideoClient VIDEO URL" -g -a KedouVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YouTubeVideoClient VIDEO URL" -g -a IIILabVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a KuKuToolVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a NoLogoVideoClient
...
# CCTV (央视网)
videodl -i "CCTV VIDEO URL" -a CCTVVideoClient
# 1905 (1905电影网)
videodl -i "M1905 VIDEO URL" -a M1905VideoClient
# BILIBILI (B站)
videodl -i "BILIBILI VIDEO URL" -a BilibiliVideoClient
videodl -i "BILIBILI VIDEO URL" -g -a VideoFKVideoClient
```

In fact, the general-purpose video parsers in the support list can be used to parse and download videos from most widely used platforms. 
The main difference is usually the resolution/quality of the downloaded video. 
If you care about video quality, you can try different general-purpose parsers, compare the results yourself, and you’re also welcome to share your findings in the repo’s Discussions section.

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

Then you can also call the video downloading function to download the video parsed by videodl. The code is as follows,

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://v.youku.com/v_show/id_XNDUxOTc1NDg4MA==.html?spm=a2hkl.14919748_WEBHOME_HOME.scg_scroll_3.d_2_play&s=faab858435f24d5bb6d3&scm=20140719.rcmd.feed.show_faab858435f24d5bb6d3&alginfo=-1reqId-249a939e8%203783%204341%2099d9%20974d2b07ad23%231764142230027-1seqId-20IX2riz0CjZG971l-1abId-2468080-1sceneId-246595&scg_id=22896555")
video_client.download(video_infos=video_infos)
```

If you want to use aria2c to accelerate the download of non-HLS/m3u8 streams, such as mp4 files, you can do the following,

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://www.bilibili.com/video/BV1KZgHzJEs6/?spm_id_from=333.337.search-card.all.click")
for v in video_infos: v['download_with_aria2c'] = True
video_client.download(video_infos=video_infos)
```

If you want to use N_m3u8DL-RE to speed up the download of HLS/m3u8 streams, you can do the following 
(*starting from videofetch 0.4.0, as long as the environment variables include N_m3u8DL-RE, the program will automatically invoke N_m3u8DL-RE to accelerate video downloads.*),

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

If you’re a VIP member of a video platform, such as Tencent Video, you can try the following code to improve the quality of the videos you download,

```python
from videodl import videodl

your_vip_cookies_with_str_or_dict_format = ""
init_video_clients_cfg = dict()
init_video_clients_cfg['TencentVideoClient'] = {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format, 'default_download_cookies': your_vip_cookies_with_str_or_dict_format}
video_client = videodl.VideoClient(init_video_clients_cfg=init_video_clients_cfg)
video_client.startparseurlcmdui()
```

Alternatively, you can run the following command directly in the terminal,

```bash
videodl -i "URL" -c "{'TencentVideoClient': {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format, 'default_download_cookies': your_vip_cookies_with_str_or_dict_format}}"
```

Of course, you can also choose a general-purpose parser that supports VIP video parsing to achieve video extraction, for example,

```bash
videodl -i "IQIYI/YOUKU/TENCENT VIDEO URL" -g -a XMFlvVideoClient
```

If you want to speed up the parsing, you can try specifying the parser used for the video you’re downloading. 
For example, when downloading a Douyin / TikTok video, you can run the command like this,

```bash
videodl -i "https://www.douyin.com/jingxuan?modal_id=7578412593719577899" -g -a "KedouVideoClient"
videodl -i "https://www.douyin.com/jingxuan?modal_id=7580605435187596559" -g -a "SnapWCVideoClient"
videodl -i "https://www.tiktok.com/@mustsharenews/video/7581408863128161552?lang=en" -g -a "SnapWCVideoClient"
```


# 💡 Recommended Projects

| Project                                                    | ⭐ Stars                                                                                                                                               | 📦 Version                                                                                                 | ⏱ Last Update                                                                                                                                                                   | 🛠 Repository                                                        |
| -------------                                              | ---------                                                                                                                                             | -----------                                                                                                | ----------------                                                                                                                                                                 | --------                                                             |
| 🎵 **Musicdl**<br/>轻量级无损音乐下载器                    | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/musicdl?style=flat-square)](https://github.com/CharlesPikachu/musicdl)                   | [![Version](https://img.shields.io/pypi/v/musicdl)](https://pypi.org/project/musicdl)                      | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/musicdl?style=flat-square)](https://github.com/CharlesPikachu/musicdl/commits/master)                   | [🛠 Repository](https://github.com/CharlesPikachu/musicdl)           |
| 🎬 **Videodl**<br/>轻量级高清无水印视频下载器              | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/videodl?style=flat-square)](https://github.com/CharlesPikachu/videodl)                   | [![Version](https://img.shields.io/pypi/v/videofetch)](https://pypi.org/project/videofetch)                | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/videodl?style=flat-square)](https://github.com/CharlesPikachu/videodl/commits/master)                   | [🛠 Repository](https://github.com/CharlesPikachu/videodl)           |
| 🖼️ **Imagedl**<br/>轻量级海量图片搜索下载器                | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/imagedl?style=flat-square)](https://github.com/CharlesPikachu/imagedl)                   | [![Version](https://img.shields.io/pypi/v/pyimagedl)](https://pypi.org/project/pyimagedl)                  | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/imagedl?style=flat-square)](https://github.com/CharlesPikachu/imagedl/commits/main)                     | [🛠 Repository](https://github.com/CharlesPikachu/imagedl)           |
| 🌐 **FreeProxy**<br/>全球海量高质量免费代理采集器          | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/freeproxy?style=flat-square)](https://github.com/CharlesPikachu/freeproxy)               | [![Version](https://img.shields.io/pypi/v/pyfreeproxy)](https://pypi.org/project/pyfreeproxy)              | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/freeproxy?style=flat-square)](https://github.com/CharlesPikachu/freeproxy/commits/master)               | [🛠 Repository](https://github.com/CharlesPikachu/freeproxy)         |
| 🌐 **MusicSquare**<br/>简易音乐搜索下载和播放网页          | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/musicsquare?style=flat-square)](https://github.com/CharlesPikachu/musicsquare)           | [![Version](https://img.shields.io/pypi/v/musicdl)](https://pypi.org/project/musicdl)                      | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/musicsquare?style=flat-square)](https://github.com/CharlesPikachu/musicsquare/commits/main)             | [🛠 Repository](https://github.com/CharlesPikachu/musicsquare)       |
| 🌐 **FreeGPTHub**<br/>真正免费的GPT统一接口                | [![Stars](https://img.shields.io/github/stars/CharlesPikachu/FreeGPTHub?style=flat-square)](https://github.com/CharlesPikachu/FreeGPTHub)             | [![Version](https://img.shields.io/pypi/v/freegpthub)](https://pypi.org/project/freegpthub)                | [![Last Commit](https://img.shields.io/github/last-commit/CharlesPikachu/FreeGPTHub?style=flat-square)](https://github.com/CharlesPikachu/FreeGPTHub/commits/main)               | [🛠 Repository](https://github.com/CharlesPikachu/FreeGPTHub)        |


# 📚 Citation

If you use this project in your research, please cite the repository.

```
@misc{videodl2021,
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


# 📱 WeChat Official Account (微信公众号)

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/videodl/master/docs/pikachu.jpg)