<div align="center">
  <img src="./docs/logo.png" width="600"/>
</div>
<br />

[![docs](https://img.shields.io/badge/docs-latest-blue)](https://videofetch.readthedocs.io/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/videofetch)](https://pypi.org/project/videofetch/)
[![PyPI](https://img.shields.io/pypi/v/videofetch)](https://pypi.org/project/videofetch)
[![license](https://img.shields.io/github/license/CharlesPikachu/videodl.svg)](https://github.com/CharlesPikachu/videodl/blob/master/LICENSE)
[![PyPI - Downloads](https://pepy.tech/badge/videofetch)](https://pypi.org/project/videofetch/)
[![issue resolution](https://isitmaintained.com/badge/resolution/CharlesPikachu/videodl.svg)](https://github.com/CharlesPikachu/videodl/issues)
[![open issues](https://isitmaintained.com/badge/open/CharlesPikachu/videodl.svg)](https://github.com/CharlesPikachu/videodl/issues)

Documents: https://videofetch.readthedocs.io/


# Videodl
```
A lightweight video downloader written by pure python.
You can star this repository to keep track of the project if it's helpful for you, thank you for your support.
```


# Statement
```
This repository is created just for learning python(Commercial prohibition).
All the apis used in this repository are from public network. So, if you want to download the paid videos, 
please open a paid member on corresponding video platform by yourself (respect the video copyright please).
Finally, if there are any infringements, please contact me to delete this repository.
```


# Support List
| Websites                                   | Introduction                                               | Code                                           |  in Chinese   |
| :----:                                     | :----:                                                     | :----:                                         |  :----:       |
| [cntv](https://v.cctv.com/)                | [click](https://mp.weixin.qq.com/s/xjl7SLEOlEbYu3d8RHZaGQ) | [click](./videodl/modules/sources/cntv.py)     |  央视网       |
| [mgtv](https://www.mgtv.com/)              | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/mgtv.py)     |  芒果TV       |
| [migu](https://www.migu.cn/video.html)     | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/migu.py)     |  咪咕视频     |
| [acfun](https://www.acfun.cn/)             | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/acfun.py)    |  AcFun视频    |
| [douyin](https://www.douyin.com/)          | [click](https://mp.weixin.qq.com/s/7N4pt1kLnVEJlve75zpdwA) | [click](./videodl/modules/sources/douyin.py)   |  抖音         |
| [haokan](https://haokan.baidu.com/)        | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw) | [click](./videodl/modules/sources/haokan.py)   |  好看视频     |
| [bilibili](https://www.bilibili.com/)      | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/bilibili.py) |  B站视频      |
| [zhihu](https://www.zhihu.com/)            | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/zhihu.py)    |  知乎视频     |
| [xigua](https://www.ixigua.com/?wid_try=1) | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/xigua.py)    |  西瓜视频     |
| [iqiyi](https://www.iqiyi.com/)            | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA) | [click](./videodl/modules/sources/iqiyi.py)    |  爱奇艺视频   |


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


# Screenshot
![img](./docs/screenshot.jpg)


# Projects in Charles_pikachu
- [Games](https://github.com/CharlesPikachu/Games): Create interesting games by pure python.
- [DecryptLogin](https://github.com/CharlesPikachu/DecryptLogin): APIs for loginning some websites by using requests.
- [Musicdl](https://github.com/CharlesPikachu/musicdl): A lightweight music downloader written by pure python.
- [Videodl](https://github.com/CharlesPikachu/videodl): A lightweight video downloader written by pure python.
- [Pytools](https://github.com/CharlesPikachu/pytools): Some useful tools written by pure python.
- [PikachuWeChat](https://github.com/CharlesPikachu/pikachuwechat): Play WeChat with itchat-uos.


# More
#### WeChat Official Accounts
*Charles_pikachu*  
![img](./docs/pikachu.jpg)