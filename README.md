<div align="center">
  <img src="https://raw.githubusercontent.com/CharlesPikachu/videodl/master/docs/logo.png" width="600"/>
</div>
<br />

<div align="center">
  <a href="https://videofetch.readthedocs.io/">
    <img src="https://img.shields.io/badge/docs-latest-blue" alt="Docs" />
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://img.shields.io/pypi/pyversions/videofetch" alt="PyPI - Python Version" />
  </a>
  <a href="https://pypi.org/project/videofetch">
    <img src="https://img.shields.io/pypi/v/videofetch" alt="PyPI" />
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-PolyForm--Noncommercial--1.0.0-blue" alt="License" />
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://static.pepy.tech/badge/videofetch" alt="PyPI - Downloads (total)">
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://static.pepy.tech/badge/videofetch/month" alt="PyPI - Downloads (month)">
  </a>
  <a href="https://pypi.org/project/videofetch/">
    <img src="https://static.pepy.tech/badge/videofetch/week" alt="PyPI - Downloads (week)">
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/actions/workflows/check_videodl.yml">
    <img src="https://github.com/CharlesPikachu/videodl/actions/workflows/check_videodl.yml/badge.svg" alt="Check Videodl Status Daily">
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/issues">
    <img src="https://isitmaintained.com/badge/resolution/CharlesPikachu/videodl.svg" alt="Issue Resolution" />
  </a>
  <a href="https://github.com/CharlesPikachu/videodl/issues">
    <img src="https://isitmaintained.com/badge/open/CharlesPikachu/videodl.svg" alt="Open Issues" />
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

- 2026-03-23: Released videofetch v0.7.0 - removed Playwright-related dependencies and replaced them with DrissionPage; improved support for parsing and downloading videos from platforms such as Xinpianchang and Kuaishou; added multiple general-purpose video parsers and downloaders; fixed several known bugs.
- 2026-03-13: Released videofetch v0.6.8 - added video parsing and downloading support for two new sites, namely, "watch.tbn.uk" and "www.abc.net.au"; optimized the implementation of "VideoInfo" data class to make IDE usage more convenient; fixed several known bugs.
- 2026-03-09: Released videofetch v0.6.7 - added a general video parser; added support for downloading videos from beacon.tv; fixed the issue where videos on Weibo might fail to download due to possible anti-leech protection; and resolved some potential bugs.


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
|                                                        | DouyinVideoClient                     | 抖音视频                           | ✔️        | ✔️       | [douyin.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/douyin.py)               |
|                                                        | DongchediVideoClient                  | 懂车帝                             | ✔️        | ✔️       | [dongchedi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/dongchedi.py)         |
|                                                        | EyepetizerVideoClient                 | 开眼视频                           | ✔️        | ✔️       | [eyepetizer.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/eyepetizer.py)       |
|                                                        | HaokanVideoClient                     | 好看视频                           | ✔️        | ✔️       | [haokan.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/haokan.py)               |
|                                                        | HuyaVideoClient                       | 虎牙视频                           | ✔️        | ✔️       | [huya.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/huya.py)                   |
|                                                        | IQiyiVideoClient                      | 爱奇艺                             | ✔️        | ✔️       | [iqiyi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/iqiyi.py)                 |
|                                                        | Ku6VideoClient                        | 酷6网                              | ✔️        | ✔️       | [ku6.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ku6.py)                     |
|                                                        | KuaishouVideoClient                   | 快手                               | ✔️        | ✔️       | [kuaishou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kuaishou.py)           |
|                                                        | KugouMVVideoClient                    | 酷狗音乐MV                         | ✔️        | ✔️       | [kugoumv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kugoumv.py)             |
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
|                                                        | ABCVideoClient                        | 澳大利亚广播公司                   | ✔️        | ✔️       | [abc.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/abc.py)                     |
|                                                        | BeaconVideoClient                     | BeaconTV                           | ✔️        | ✔️       | [beacon.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/beacon.py)               |
|                                                        | CCCVideoClient                        | CCC视频 (黑客大会视频)             | ✔️        | ✔️       | [ccc.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ccc.py)                     |
|                                                        | FoxNewsVideoClient                    | 福克斯新闻                         | ✔️        | ✔️       | [foxnews.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/foxnews.py)             |
|                                                        | PlusFIFAVideoClient                   | FIFA+平台 (国际足联+)              | ✔️        | ✔️       | [plusfifa.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/plusfifa.py)           |
|                                                        | GeniusVideoClient                     | Rap Genius (嘻哈百科)              | ✔️        | ✔️       | [genius.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/genius.py)               |
|                                                        | KakaoVideoClient                      | KakaoTV                            | ✔️        | ✔️       | [kakao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kakao.py)                 |
|                                                        | RedditVideoClient                     | 红迪网                             | ✔️        | ✔️       | [reddit.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/reddit.py)               |
|                                                        | TBNUKVideoClient                      | 英国三一电视台点播网站             | ✔️        | ✔️       | [tbnuk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/tbnuk.py)                 |
|                                                        | TedVideoClient                        | TED视频                            | ✔️        | ✔️       | [ted.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ted.py)                     |
|                                                        | UnityVideoClient                      | Unity                              | ✔️        | ✔️       | [unity.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/unity.py)                 |
|                                                        | WWEVideoClient                        | 世界摔角娱乐                       | ✔️        | ✔️       | [wwe.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wwe.py)                     |
|                                                        | WittyTVVideoClient                    | Witty TV (意大利多媒体娱乐平台)    | ✔️        | ✔️       | [wittytv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wittytv.py)             |
|                                                        | YouTubeVideoClient                    | 油管视频                           | ✔️        | ✔️       | [youtube.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youtube.py)             |

To make videodl more robust and able to adaptively parse videos from more websites, even when the video URL is not in the supported list above, 
I also plan to gradually add some general-purpose parsing interfaces. The currently supported generic parsers include,

| CommonVideoClient (EN)                                            | CommonVideoClient (CN)                                                  | ParseURL | Download | Core Code                                                                                                   |
| :--------------------------------------------------------------   | :-------------------------------------------------------------          | :-----:  | :-----:  | :---------------------------------------------------------------------------------------------------------- |
| [AnyFetcherVideoClient](https://anyfetcher.com/zh-cn)             | [万能视频下载器](https://anyfetcher.com/zh-cn)                          |   ✔️     |   ✔️     | [anyfetcher.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/anyfetcher.py) |
| [BVVideoClient](https://www.bestvideow.com/xhs)                   | [BestVideo下载器](https://www.bestvideow.com/xhs)                       |   ✔️     |   ✔️     | [bv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/bv.py)                 |
| [BugPkVideoClient](https://sv.bugpk.com/)                         | [短视频解析工具](https://sv.bugpk.com/)                                 |   ✔️     |   ✔️     | [bugpk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/bugpk.py)           |
| [GVVideoClient](https://greenvideo.cc/)                           | [GreenVideo视频下载](https://greenvideo.cc/)                            |   ✔️     |   ✔️     | [gv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/gv.py)                 |
| [GVVIPVideoClient](https://greenvideo.cc/video/vip)               | [GreenVideoVIP视频解析](https://greenvideo.cc/video/vip)                |   ✔️     |   ✔️     | [gvvip.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/gvvip.py)           |
| [IIILabVideoClient](https://roar.iiilab.com/)                     | [兽音译者](https://roar.iiilab.com/)                                    |   ✔️     |   ✔️     | [iiilab.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/iiilab.py)         |
| [IM1907VideoClient](https://im1907.top/)                          | [IM1907电影解析网](https://im1907.top/)                                 |   ✔️     |   ✔️     | [im1907.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/im1907.py)         |
| [KedouVideoClient](https://www.kedou.life/)                       | [Kedou视频解析](https://www.kedou.life/)                                |   ✔️     |   ✔️     | [kedou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/kedou.py)           |
| [KuKuToolVideoClient](https://dy.kukutool.com/)                   | [KuKuTool视频解析](https://dy.kukutool.com/)                            |   ✔️     |   ✔️     | [kukutool.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/kukutool.py)     |
| [KIT9VideoClient](https://apis.kit9.cn/api/aggregate_videos/)     | [聚合短视频解析](https://apis.kit9.cn/api/aggregate_videos/)            |   ✔️     |   ✔️     | [kit9.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/kit9.py)             |
| [LongZhuVideoClient](https://www.hhlqilongzhu.cn/H5_home.php)     | [龙珠API视频解析](https://www.hhlqilongzhu.cn/H5_home.php)              |   ✔️     |   ✔️     | [longzhu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/longzhu.py)       |
| [LvlongVideoClient](https://jcy.lvlong.xyz/jxr.php)               | [绿龙解析](https://jcy.lvlong.xyz/jxr.php)                              |   ✔️     |   ✔️     | [lvlong.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/lvlong.py)         |
| [MiZhiVideoClient](https://api.98dou.cn/doc/video_qsy/juhe.html)  | [觅知聚合短视频去水印](https://api.98dou.cn/doc/video_qsy/juhe.html)    |   ✔️     |   ✔️     | [mizhi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/mizhi.py)           |
| [NoLogoVideoClient](https://nologo.code24.top/)                   | [去水印下载鸭](https://nologo.code24.top/)                              |   ✔️     |   ✔️     | [nologo.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/nologo.py)         |
| [ODwonVideoClient](https://odown.cc/cctv)                         | [橙子解析](https://odown.cc/cctv)                                       |   ✔️     |   ✔️     | [odown.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/odown.py)           |
| [PVVideoClient](https://www.parsevideo.com/)                      | [在线视频解析工具](https://www.parsevideo.com/)                         |   ✔️     |   ✔️     | [pv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/pv.py)                 |
| [QingtingVideoClient](https://33tool.com/video_parse/)            | [蜻蜓工具](https://33tool.com/video_parse/)                             |   ✔️     |   ✔️     | [qingting.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/qingting.py)     |
| [QZXDPToolsVideoClient](https://tools.qzxdp.cn/video_spider)      | [全栈工具视频解析](https://tools.qzxdp.cn/video_spider)                 |   ✔️     |   ✔️     | [qzxdptools.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/qzxdptools.py) |
| [QwkunsVideoClient](https://qwkuns.me/)                           | [Qwkuns视频解析 (基于Cobalt)](https://qwkuns.me/)                       |   ✔️     |   ✔️     | [qwkuns.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/qwkuns.py)         |
| [RayVideoClient](https://www.raydownloader.com/)                  | [飞鱼视频下载助手](https://www.raydownloader.com/)                      |   ✔️     |   ✔️     | [ray.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/ray.py)               |
| [SnapAnyVideoClient](https://snapany.com/zh)                      | [SnapAny万能解析](https://snapany.com/zh)                               |   ✔️     |   ✔️     | [snapany.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/snapany.py)       |
| [SnapWCVideoClient](https://snapwc.com/zh)                        | [SnapWC视频解析](https://snapwc.com/zh)                                 |   ✔️     |   ✔️     | [snapwc.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/snapwc.py)         |
| [SENJiexiVideoClient](https://jiexi.789jiexi.icu:4433/)           | [789视频解析](https://jiexi.789jiexi.icu:4433/)                         |   ✔️     |   ✔️     | [senjiexi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/senjiexi.py)     |
| [VgetVideoClient](https://vget.xyz/)                              | [Vget视频解析](https://vget.xyz/)                                       |   ✔️     |   ✔️     | [vget.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/vget.py)             |
| [VideoFKVideoClient](https://www.videofk.com/)                    | [免费短视频下载器](https://www.videofk.com/)                            |   ✔️     |   ✔️     | [videofk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/videofk.py)       |
| [WoofVideoClient](https://dl.woof.monster/)                       | [Woof视频解析 (基于Cobalt)](https://dl.woof.monster/)                   |   ✔️     |   ✔️     | [woof.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/woof.py)             |
| [XiazaitoolVideoClient](https://www.xiazaitool.com/dy)            | [下载狗](https://www.xiazaitool.com/dy)                                 |   ✔️     |   ✔️     | [xiazaitool.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xiazaitool.py) |
| [XMFlvVideoClient](https://jx.xmflv.com/)                         | [虾米解析](https://jx.xmflv.com/)                                       |   ✔️     |   ✔️     | [xmflv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xmflv.py)           |
| [XCVTSVideoClient](https://api.xcvts.cn/)                         | [小尘聚合短视频去水印](https://api.xcvts.cn/)                           |   ✔️     |   ✔️     | [xcvts.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xcvts.py)           |
| [XZDXVideoClient](https://xzdx.top/#/pages/duan/duan)             | [小众独行助手](https://xzdx.top/#/pages/duan/duan)                      |   ✔️     |   ✔️     | [xzdx.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xzdx.py)             |
| [XiaolvfangVideoClient](https://www.xiaolvfang.com/)              | [效率坊](https://www.xiaolvfang.com/)                                   |   ✔️     |   ✔️     | [xiaolvfang.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/xiaolvfang.py) |
| [ZanqianbaVideoClient](https://www.zanqianba.com/)                | [考拉解析](https://www.zanqianba.com/)                                  |   ✔️     |   ✔️     | [zanqianba.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/zanqianba.py)   |

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
  N_m3u8DL-RE is a specialized m3u8 downloader that adds extensive logic for handling encryption, anti-leech headers, redirects, and malformed playlists, so it can capture many "protected" or non-standard videos that FFmpeg fails on. 
  In many cases it’s also faster, because N_m3u8DL-RE can download HLS segments in parallel with optimized retries/merging, while FFmpeg typically pulls segments sequentially by default.
  ❗ **Therefore, we recommend that all videodl users install N_m3u8DL-RE to ensure videodl delivers the best possible performance.** ❗
  You can skip installing it, but videodl may then be unable to parse some platforms, including but not limited to,
  ```
  CCTVVideoClient, FoxNewsVideoClient, TencentVideoClient, GVVIPVideoClient, 
  SnapAnyVideoClient, VgetVideoClient, ArteTVVideoClient, XMFlvVideoClient, 
  RedditVideoClient, IIILabVideoClient, WWEVideoClient, IQiyiVideoClient,
  PlusFIFAVideoClient, IM1907VideoClient, M1905VideoClient, SENJiexiVideoClient, etc.
  ```
  and downloads from many other sites that provide m3u8/HLS streams may also be significantly limited.
  As with FFmpeg, after installation you should make sure this tool can be run directly from the command line, *i.e.*, its location is included in your system `PATH`.
  A quick way to check whether N_m3u8DL-RE has been installed successfully is to open a terminal (or Command Prompt on Windows) and run,
  ```bash
  N_m3u8DL-RE --version
  ```
  If N_m3u8DL-RE is installed correctly, `N_m3u8DL-RE --version` will print the N_m3u8DL-RE version (*e.g.*, `0.5.1+c1f6db5639397dde362c31b31eebd88c796c90da`).
  If you see a similar `command not found` / `not recognized` error, N_m3u8DL-RE is not installed correctly or not available on your `PATH`.

- **[Node.js](https://nodejs.org/en)**: Currently, Node.js is only used in `YouTubeVideoClient`, `CCTVVideoClient` and `TencentVideoClient` to execute certain JavaScript code for video parsing. 
  Therefore, if you don’t need to use `YouTubeVideoClient`, `CCTVVideoClient` and `TencentVideoClient`, you can safely skip installing this CLI tool.
  A quick way to check whether Node.js has been installed successfully is to open a terminal and run,
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

Or just run `videodl -i "URL"` (maybe `videodl --help` to show usage information) from the terminal,

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

#### Recommended Parsing Commands for Common Streaming Platforms

Recommended parsing and downloading commands for some widely used video platforms are as follows,

```bash
# IQIYI / YOUKU / TENCENT / PPTV / MGTV / CCTV / BILIBILI (爱奇艺, 优酷, 腾讯视频, PPTV, 芒果TV, CCTV, B站等平台的电影电视剧)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a IM1907VideoClient (Recommended, 1080p)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a SENJiexiVideoClient (Recommended)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a XMFlvVideoClient
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a GVVIPVideoClient
videodl -i "YOUKU/TENCENT" -g -a LvlongVideoClient
# Examples
videodl -i "https://www.iqiyi.com/v_cy4phe8b08.html" -g -a IM1907VideoClient
videodl -i "https://v.qq.com/x/cover/mzc002001nl46xm/t410130yz0y.html" -g -a IM1907VideoClient
# Please Note
Since the parsing relies on a third-party online parsing API, the downloaded video may contain inserted advertisements. 
These ads are not added by videodl, they are inserted by the online parsing website. 
We recommend using ffmpeg to trim out the ad segments. (example code see ./scripts/ffmpeg_segment_remover.py)

# MIGU (咪咕视频)
videodl -i "MIGU VIDEO URL" -g -a RayVideoClient
videodl -i "MIGU VIDEO URL" -g -a KedouVideoClient
# Examples
videodl -i "https://www.miguvideo.com/p/detail/759959727" -g -a KedouVideoClient

# DOUYIN / TIKTOK / KUAISHOU / XIAOHONGSHU / YOUTUBE / FACEBOOK / TITTER (X) (抖音, 抖音海外, 快手, 小红书, 油管, 脸书, 推特视频等)
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a VideoFKVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a SnapAnyVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a GVVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a AnyFetcherVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a IIILabVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a VgetVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a SnapWCVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a KedouVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a KuKuToolVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a XiaolvfangVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a XZDXVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a KIT9VideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a QZXDPToolsVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a NoLogoVideoClient
# Examples
videodl -i "https://www.douyin.com/jingxuan?modal_id=7569541184671974899" -g -a SnapAnyVideoClient
videodl -i "https://www.tiktok.com/@pet_statione/video/7579841364599328013?lang=en" -g -a SnapAnyVideoClient

# 1905 (1905电影网)
videodl -i "M1905 VIDEO URL" -a M1905VideoClient
# Examples
videodl -i "https://www.1905.com/video/play/1751538.shtml" -a M1905VideoClient

# XINPIANCHANG (新片场)
videodl -i "XINPIANCHANG VIDEO URL" -a XinpianchangVideoClient
# Examples
videodl -i "https://www.xinpianchang.com/a13536060?from=IndexPick&part=%E7%BC%96%E8%BE%91%E7%B2%BE%E9%80%89&index=1" -a XinpianchangVideoClient

# BILIBILI (B站)
videodl -i "BILIBILI VIDEO URL" -a BilibiliVideoClient
videodl -i "BILIBILI VIDEO URL" -g -a VideoFKVideoClient
# Examples
videodl -i "https://www.bilibili.com/video/BV13x41117TL" -a BilibiliVideoClient
videodl -i "https://www.bilibili.com/video/BV1bK411W797?p=1" -a BilibiliVideoClient
videodl -i "https://www.bilibili.com/bangumi/play/ep21495" -a BilibiliVideoClient
videodl -i "https://www.bilibili.com/video/av8903802/" -a BilibiliVideoClient

# CCTV (央视网)
videodl -i "CCTV VIDEO URL" -a CCTVVideoClient
# Examples
videodl -i "https://v.cctv.com/2026/01/09/VIDE0ifonRhsuR952gJ3zUKu260109.shtml?spm=C90324.PE6LRxWJhH5P.S23920.3" -a CCTVVideoClient

# PLUSFIFA (国际足联+比赛视频)
videodl -i "PLUSFIFA VIDEO URL" -a PlusFIFAVideoClient
# Examples
videodl -i "https://www.plus.fifa.com/en/content/fc-sochaux-montbeliard-vs-lb-chateauroux/6ff75563-c6fc-4b08-b324-54771dbd7029" -a PlusFIFAVideoClient
```

In practice, the general-purpose video parsers listed under [Supported Video Client](https://github.com/CharlesPikachu/videodl/tree/master?tab=readme-ov-file#-supported-video-client) can handle parsing and downloading videos from most major platforms. 
The main difference typically comes down to the maximum resolution and overall output quality. 
If video quality matters to you, feel free to try a few different parsers and compare the results. 
And if you discover anything useful, you’re welcome to share your findings in the repo’s [Discussions section](https://github.com/CharlesPikachu/videodl/discussions).

#### Parsing and Downloading as Separate Steps

If you just want to parse a video link and retrieve information about the video, you can do it like this,

```python
from videodl import videodl

# set allowed_video_sources to select the clients used for parsing the URL.
video_client = videodl.VideoClient(allowed_video_sources=['YoukuVideoClient'])
# parse from url
video_infos = video_client.parsefromurl("https://v.youku.com/v_show/id_XNDUxOTc1NDg4MA==.html")
# print parse results
print(video_infos)
```

The output of this code looks like,

```python
[
  {
    "source": "YoukuVideoClient",
    "raw_data": {},
    "download_url": "http://pl-ali.youku.com/playlist/m3u8?vid=XNDUxOTc1NDg4MA%3D%3D&type=mp4hd2v3&ups_client_netip=725c13c1&utid=Mu3nIfZs0CsCAXJcE8F2Zepy&ccode=0564&psid=9f0ebc4bd03a063e9f543b0f1142b2c041346&duration=2205&expire=18000&drm_type=1&drm_device=0&drm_default=1&dyt=0&ups_ts=1767964466&onOff=0&encr=0&ups_key=c0632ee975ef2dacc2118d9130573bd5&ckt=3&m_onoff=0&pn=&drm_type_value=default&v=v1&bkp=0",
    "title": "史家绝唱",
    "file_path": "videodl_outputs\\YoukuVideoClient\\史家绝唱.m3u",
    "ext": "m3u",
    "err_msg": "",
    "download_with_ffmpeg": true,
    "download_with_aria2c": false,
    "enable_nm3u8dlre": false,
    "identifier": "XNDUxOTc1NDg4MA==",
    "guess_video_ext_result": {
      "ext": "m3u",
      "sniffer": "requests.head",
      "ok": true
    },
    "audio_download_url": "",
    "guess_audio_ext_result": {},
    "audio_ext": "m4a",
    "audio_file_path": "",
    "default_download_headers": null,
    "default_download_cookies": null
  }
]
```

Then you can also call the video downloading function to download the video parsed by videodl. The code is as follows,

```python
from videodl import videodl

video_client = videodl.VideoClient(allowed_video_sources=['YoukuVideoClient'])
video_infos = video_client.parsefromurl("https://v.youku.com/v_show/id_XNDUxOTc1NDg4MA==.html")
video_client.download(video_infos=video_infos)
```

#### Parse and Download Speedup

To reduce parsing time, you can specify which parser to use for the video you’re downloading, *i.e.*,

```bash
videodl -i "BILIBILI VIDEO URL" -a BilibiliVideoClient
```

is better than,

```bash
videodl -i "BILIBILI VIDEO URL"
```

If you know the video URL you want to parse is not covered by the platform-specific clients and you’d like to use a generic parser directly, set `apply_common_video_clients_only` to `True`.
For example, you can run `videodl -i "URL" -g` in the terminal, or do the same in code as shown below,

```python
from videodl import videodl

video_client = videodl.VideoClient(apply_common_video_clients_only=True)
video_client.startparseurlcmdui()
```

Better yet, specify the generic parser you want to use. For example, to download a Douyin/TikTok video, run,

```bash
videodl -i "https://www.douyin.com/jingxuan?modal_id=7578412593719577899" -g -a "KedouVideoClient"
videodl -i "https://www.douyin.com/jingxuan?modal_id=7580605435187596559" -g -a "SnapWCVideoClient"
videodl -i "https://www.tiktok.com/@mustsharenews/video/7581408863128161552?lang=en" -g -a "SnapWCVideoClient"
```

If you want to use aria2c to accelerate the download of non-HLS/m3u8 streams, such as mp4 files, you can do the following,

```python
from videodl import videodl

video_client = videodl.VideoClient(allowed_video_sources=['BilibiliVideoClient'])
video_infos = video_client.parsefromurl("https://www.bilibili.com/bangumi/play/ss26801")
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

#### VIP / Premium Video Parsing

For VIP (premium) video links, you have two options to parse and download the video. 

The first option is to use a third-party parsing service. 
For example, for an IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL (Movies and TV shows), you can run the following command,

```bash
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a IM1907VideoClient (Recommended, 1080p)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a SENJiexiVideoClient (Recommended)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a XMFlvVideoClient
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a GVVIPVideoClient
videodl -i "YOUKU/TENCENT" -g -a LvlongVideoClient
```

Of course, it’s worth noting that this approach may come with some drawbacks, for example, some third-party parsing services may occasionally insert a few seconds of unwanted ads into the downloaded video.
These ads are not added by videodl, they are inserted by the online parsing website. 
We recommend using ffmpeg to trim out the ad segments ([Example Script](https://github.com/CharlesPikachu/videodl/blob/master/scripts/ffmpeg_segment_remover.py)).

The second option is to parse and download VIP (premium) videos directly via the platform’s native APIs (you’ll need to provide cookies from an account logged in with an active membership on that platform),

```python
from videodl import videodl

your_vip_cookies_with_str_or_dict_format = ""
init_video_clients_cfg = dict()
init_video_clients_cfg['IQiyiVideoClient'] = {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format}
video_client = videodl.VideoClient(init_video_clients_cfg=init_video_clients_cfg, allowed_video_sources=['IQiyiVideoClient'])
video_client.startparseurlcmdui()
```

Alternatively, you can run the following command directly in the terminal,

```bash
videodl -i "URL" -c "{'IQiyiVideoClient': {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format}}" -a IQiyiVideoClient
```

If the code above can successfully extract the VIP video URL but the download fails, try also passing your membership cookies during the download step,

```python
from videodl import videodl

your_vip_cookies_with_str_or_dict_format = ""
init_video_clients_cfg = dict()
init_video_clients_cfg['TencentVideoClient'] = {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format, 'default_download_cookies': your_vip_cookies_with_str_or_dict_format}
video_client = videodl.VideoClient(init_video_clients_cfg=init_video_clients_cfg, allowed_video_sources=['TencentVideoClient'])
video_client.startparseurlcmdui()
```

Alternatively, you can run the following command directly in the terminal,

```bash
videodl -i "URL" -c "{'TencentVideoClient': {'default_parse_cookies': your_vip_cookies_with_str_or_dict_format, 'default_download_cookies': your_vip_cookies_with_str_or_dict_format}}" -a TencentVideoClient
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