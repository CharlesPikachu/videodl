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

| VideoClient (EN)                      |  VideoClient (CN)          | WeChat Article                                              | Search   |  ParseURL  |  Download  | Core Code                                                                                                              |
| :----:                                |  :----:                    | :----:                                                      | :----:   |  :----:    |  :----:    | :----:                                                                                                                 |
| AcFunVideoClient                      |  A站                       | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw)  | ❌       |  ✔️        |  ✔️        | [acfun.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/acfun.py)                     |
| PipigaoxiaoVideoClient                |  皮皮搞笑                  | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [pipigaoxiao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipigaoxiao.py)         |
| PipixVideoClient                      |  皮皮虾                    | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [pipix.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipix.py)                     |
| HaokanVideoClient                     |  好看视频                  | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw)  | ❌       |  ✔️        |  ✔️        | [haokan.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/haokan.py)                   |
| TedVideoClient                        |  TED视频 (演讲视频)        | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [ted.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ted.py)                         |
| Ku6VideoClient                        |  酷6网                     | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [ku6.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ku6.py)                         |
| BilibiliVideoClient                   |  哔哩哔哩 (B站)            | [click](https://mp.weixin.qq.com/s/yNUhMlRs5N4iUfpmo2LXMA)  | ❌       |  ✔️        |  ✔️        | [bilibili.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/bilibili.py)               |
| KuaishouVideoClient                   |  快手                      | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [kuaishou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kuaishou.py)               |
| YinyuetaiVideoClient                  |  音悦台 (官网倒闭ing😭)    | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [yinyuetai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/yinyuetai.py)             |
| BaiduTiebaVideoClient                 |  百度贴吧                  | [click](https://mp.weixin.qq.com/s/_lbS4t1uSTRAV2Or-oCDpQ)  | ❌       |  ✔️        |  ✔️        | [baidutieba.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/baidutieba.py)           |
| MGTVkanVideoClient                    |  芒果TV                    | [click](https://mp.weixin.qq.com/s/H4w-wjMqi44uNTynGfkKvw)  | ❌       |  ✔️        |  ✔️        | [mgtv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/mgtv.py)                       |
| OasisVideoClient                      |  新浪绿洲                  | -                                                           | ❌       |  ✔️        |  ✔️        | [oasis.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/oasis.py)                     |
| PearVideoClient                       |  梨视频                    | -                                                           | ❌       |  ✔️        |  ✔️        | [pear.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pear.py)                       |
| HuyaVideoClient                       |  虎牙视频                  | -                                                           | ❌       |  ✔️        |  ✔️        | [huya.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/huya.py)                       |

The links used during testing are listed below,

```python
VIDEO_SAMPLES = {
    'AcFunVideoClient': [
        'https://www.acfun.cn/v/ac29566205', 
        'https://www.acfun.cn/v/ac47998293', 
        'https://www.acfun.cn/v/ac36491489'
    ],
    'HaokanVideoClient': [
        'https://haokan.baidu.com/v?vid=7295039339702288421', 
        'https://haokan.baidu.com/v?vid=7224830823778858146'
    ],
    'TedVideoClient': [
        'https://www.ted.com/talks/alanna_shaikh_why_covid_19_is_hitting_us_now_and_how_to_prepare_for_the_next_outbreak', 
        'https://www.ted.com/talks/adam_kucharski_how_can_we_control_the_coronavirus_pandemic'
    ],
    'PipigaoxiaoVideoClient': [
        'https://h5.ippzone.com/pp/post/350259149175?zy_to=copy_link&share_count=1&m=0cd13da8548a1bc85813d8c60d331e22&app=&type=post&did=d2bddf23159ae495&mid=1270840711117&pid=350259149175',
        'https://h5.ippzone.com/pp/post/870235406308?app=&did=d2bddf23159ae495&m=0cd13da8548a1bc85813d8c60d331e22&mid=1270840711117&pid=870235406308&share_count=1&type=post&zy_to=copy_link'
    ],
    'PipixVideoClient': [
        'https://h5.pipix.com/item/6740623460659108107?app_id=1319&app=super&timestamp=1574241444&user_id=1085910221863021&carrier_region=cn&region=cn&language=zh&utm_source=weixin',
        'https://h5.pipix.com/item/6863294377570081027?app_id=1319&app=super&timestamp=1598011674&user_id=62108092335&carrier_region=cn&region=cn&language=zh&utm_source=weixin'
    ],
    'Ku6VideoClient': [
        'https://www.ku6.com/video/detail?id=McZoSe_hgG_jwzy7pQLqvMJ3IoI.', 
        'https://www.ku6.com/video/detail?id=HE3lfhcp13Gd0qND4zfzXYQONMY.'
    ],
    'KuaishouVideoClient': [
        'https://www.kuaishou.com/short-video/3xwzr5dveyqc5fa?authorId=3xv7d3j7hqqpksi', 
        'https://www.kuaishou.com/short-video/3xjpwzyparcgnck?authorId=3xbbsmxr7cdmhqs'
    ],
    'BilibiliVideoClient': [
        'https://www.bilibili.com/video/BV16Z4y1X784/?spm_id_from=333.851.b_7265636f6d6d656e64.2', 
        'https://www.bilibili.com/video/BV1KZgHzJEs6/?spm_id_from=333.337.search-card.all.click'
    ],
    'YinyuetaiVideoClient': [
        'https://www.yinyuetai.com/watch/7200480383631265792?listType=swiper&listId=6998475633361805312'
    ],
    'BaiduTiebaVideoClient': [
        'https://tieba.baidu.com/p/6098286801', 
        'https://tieba.baidu.com/p/7280373361'
    ],
    'MGTVkanVideoClient': [
        'https://www.mgtv.com/l/100026064/19868457.html?fpa=1684&fpos=&lastp=ch_home&cpid=5',
        'https://www.mgtv.com/b/788366/23780111.html?fpa=1756&fpos=&lastp=ch_home', # requires pass VIP login-in cookies by default_parse_cookies and default_download_cookies to download full video
        'https://www.mgtv.com/b/805972/23756299.html?fpa=1261&fpos=&lastp=ch_home&cpid=5', # requires pass login-in cookies by default_download_cookies to download full video
    ],
}
```


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

Also, some video downloaders depend on [Ffmpeg](https://ffmpeg.org/) and [Node.js](https://nodejs.org/en/), so please make sure to install them before using videodl.


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


# 📱 WeChat Official Account (微信公众号):

Charles的皮卡丘 (*Charles_pikachu*)  
![img](https://raw.githubusercontent.com/CharlesPikachu/videodl/master/docs/pikachu.jpg)