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
    <img src="https://pepy.tech/badge/videofetch" alt="PyPI - Downloads" />
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://img.shields.io/pypi/dm/videofetch?style=flat-square" alt="downloads" />
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


# 🚀 Introduction

A fast and lightweight video downloader built entirely in Python! 🚀 
If you find this project useful, don't forget to star the repository and help us grow—your support means the world! 🙌


# 📜 Statement

This repository is created solely for learning purposes (commercial use is prohibited). 
All APIs used here are sourced from public networks. 
If you wish to download paid videos, please ensure you have a paid membership on the respective video platform (respect copyright, please!). 
If any content in this repository causes concerns or infringes on copyright, please reach out to me, and I’ll promptly remove it.


# Support List
| Source_EN                                                  |  Source_CN    | Introduction                                               | Core Code                                              |
| :----:                                                     |  :----:       | :----:                                                     | :----:                                                 |
| [cntv](https://v.cctv.com/)                                |  央视网       | [click](https://mp.weixin.qq.com/s/xjl7SLEOlEbYu3d8RHZaGQ) | [click](./videodl/modules/sources/cntv.py)             |
| [mgtv](https://www.mgtv.com/)                              |  芒果TV       | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/mgtv.py)             |
| [migu](https://www.migu.cn/video.html)                     |  咪咕视频     | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/migu.py)             |
| [acfun](https://www.acfun.cn/)                             |  AcFun视频    | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/acfun.py)            |
| [douyin](https://www.douyin.com/)                          |  抖音         | [click](https://mp.weixin.qq.com/s/7N4pt1kLnVEJlve75zpdwA) | [click](./videodl/modules/sources/douyin.py)           |
| [haokan](https://haokan.baidu.com/)                        |  好看视频     | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/haokan.py)           |
| [bilibili](https://www.bilibili.com/)                      |  B站视频      | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/bilibili.py)         |
| [zhihu](https://www.zhihu.com/)                            |  知乎视频     | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/zhihu.py)            |
| [xigua](https://www.ixigua.com/?wid_try=1)                 |  西瓜视频     | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/xigua.py)            |
| [iqiyi](https://www.iqiyi.com/)                            |  爱奇艺视频   | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/iqiyi.py)            |
| [ted](https://www.ted.com/)                                |  TED视频      | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/ted.py)              |
| [pipigaoxiao](https://h5.ippzone.com/pp/post/78266943052)  |  皮皮搞笑     | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/pipigaoxiao.py)      |
| [pipix](https://www.pipix.com/)                            |  皮皮虾       | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/pipix.py)            |
| [yinyuetai](https://www.yinyuetai.com/)                    |  音悦网       | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/yinyuetai.py)        |
| [weibo](https://m.weibo.cn/)                               |  微博         | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/weibo.py)            |
| [baidutieba](https://tieba.baidu.com/index.html)           |  百度贴吧     | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/baidutieba.py)       |
| [kuaishou](https://www.kuaishou.com/)                      |  快手视频     | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/kuaishou.py)         |
| [ku6](https://www.ku6.com/index)                           |  酷6网        | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/ku6.py)              |
| [sohu](https://tv.sohu.com/)                               |  搜狐TV       | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ) | [click](./videodl/modules/sources/sohu.py)             |


# Install

#### Preparation
- [ffmpeg](https://ffmpeg.org/): You should set ffmpeg in environment variable.
- [Nodejs](https://nodejs.org/en/): Since some of the supported websites (e.g., xigua) need to compile the js code, you should install the nodejs in your computer.

#### Pip install
```sh
run "pip install videofetch"
```

#### Source code install
```sh
(1) Offline
Step1: git clone https://github.com/CharlesPikachu/videodl.git
Step2: cd videodl -> run "python setup.py install"
(2) Online
run "pip install git+https://github.com/CharlesPikachu/videodl.git@master"
```


# Quick Start

#### Run by leveraging the API

```python
from videodl import videodl

config = {
    "logfilepath": "videodl.log",
    "proxies": {},
    "savedir": "downloaded"
}
dl_client = videodl.videodl(config=config)
dl_client.run()
```

#### Run by leveraging compiled file

```sh
Usage: videodl [OPTIONS]

Options:
  -i, --url TEXT          想要下载的视频链接, 若不指定, 则进入videodl终端版
  -l, --logfilepath TEXT  日志文件保存的路径
  -p, --proxies TEXT      设置的代理
  -s, --savedir TEXT      视频保存的文件夹
  --help                  Show this message and exit.
```


# Screenshot
![img](./docs/screenshot.gif)


# Projects in Charles_pikachu
- [Games](https://github.com/CharlesPikachu/Games): Create interesting games by pure python.
- [DecryptLogin](https://github.com/CharlesPikachu/DecryptLogin): APIs for loginning some websites by using requests.
- [Musicdl](https://github.com/CharlesPikachu/musicdl): A lightweight music downloader written by pure python.
- [Videodl](https://github.com/CharlesPikachu/videodl): A lightweight video downloader written by pure python.
- [Pytools](https://github.com/CharlesPikachu/pytools): Some useful tools written by pure python.
- [PikachuWeChat](https://github.com/CharlesPikachu/pikachuwechat): Play WeChat with itchat-uos.
- [Pydrawing](https://github.com/CharlesPikachu/pydrawing): Beautify your image or video.
- [ImageCompressor](https://github.com/CharlesPikachu/imagecompressor): Image compressors written by pure python.
- [FreeProxy](https://github.com/CharlesPikachu/freeproxy): Collecting free proxies from internet.
- [Paperdl](https://github.com/CharlesPikachu/paperdl): Search and download paper from specific websites.
- [Sciogovterminal](https://github.com/CharlesPikachu/sciogovterminal): Browse "The State Council Information Office of the People's Republic of China" in the terminal.
- [CodeFree](https://github.com/CharlesPikachu/codefree): Make no code a reality.
- [DeepLearningToys](https://github.com/CharlesPikachu/deeplearningtoys): Some deep learning toys implemented in pytorch.
- [DataAnalysis](https://github.com/CharlesPikachu/dataanalysis): Some data analysis projects in charles_pikachu.
- [Imagedl](https://github.com/CharlesPikachu/imagedl): Search and download images from specific websites.
- [Pytoydl](https://github.com/CharlesPikachu/pytoydl): A toy deep learning framework built upon numpy.
- [NovelDL](https://github.com/CharlesPikachu/noveldl): Search and download novels from some specific websites.


# More
#### WeChat Official Accounts
*Charles_pikachu*  
![img](./docs/pikachu.jpg)