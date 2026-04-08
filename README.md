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

- 2026-04-03: Released videofetch v0.8.1 - improved the downloadable video quality in the YouTube video client; added a native API for LeTV video parsing and downloading; added a general-purpose parsing API.
- 2026-04-02: Released videofetch v0.8.0 - refactored the base video client class to make the video downloading logic clearer and more extensible; refactored the video info class to provide more comprehensive functionality and more IDE-friendly hints; fixed bugs and invalidation issues in multiple supported video clients.
- 2026-03-27: Released videofetch v0.7.2 - added a new general-purpose video parsing interface; added support for video parsing and downloading from the player.pl site; fixed some potential bugs.


# 🚀 Introduction

A fast, lightweight, and fully Python-based video downloader built for simplicity, efficiency, and flexibility. 🚀
Whether used in academic research to collect and organize video data for dataset construction, in development workflows for multimedia processing pipelines, or in personal projects to save online videos for offline access where permitted, this project provides a clean and practical solution without unnecessary bloat.
With an easy-to-understand Python codebase and lightweight design, it is suitable both for direct use and for further extension in custom applications.
If this project helps with work, research, or everyday use, please consider giving it a star ⭐ — your support helps more people discover the project and motivates future improvements. 🙌


# 📜 Statement

This repository is created solely for learning purposes (commercial use is prohibited). 
All APIs used here are sourced from public networks. 
If you wish to download paid videos, please ensure you have a paid membership on the respective video platform (respect copyright, please!). 
If any content in this repository causes concerns or infringes on copyright, please reach out to me, and I’ll promptly remove it.


# 🎥 Supported Video Client

The video platforms currently supported for parsing are,

| Category                                               | VideoClient (EN)                                                 | VideoClient (CN)                                                      | ParseURL  | Download | Core Code                                                                                                          |
| :--                                                    | :--                                                              | :--                                                                   | :--:      | :--:     | :--                                                                                                                |
| **Chinese Platforms**                                  | [AcFunVideoClient](https://www.acfun.cn)                         | [A站](https://www.acfun.cn)                                           | ✔️        | ✔️       | [acfun.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/acfun.py)                 |
|                                                        | BaiduTiebaVideoClient                 | 百度贴吧                           | ✔️        | ✔️       | [baidutieba.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/baidutieba.py)       |
|                                                        | BilibiliVideoClient                   | 哔哩哔哩 (B站)                     | ✔️        | ✔️       | [bilibili.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/bilibili.py)           |
|                                                        | C56VideoClient                        | 56视频网                           | ✔️        | ✔️       | [c56.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/c56.py)                     |
|                                                        | CCTVVideoClient                       | 央视网                             | ✔️        | ✔️       | [cctv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/cctv.py)                   |
|                                                        | CCtalkVideoClient                     | CCtalk                             | ✔️        | ✔️       | [cctalk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/cctalk.py)               |
|                                                        | [ChinaDailyVideoClient](https://cn.chinadaily.com.cn/)           | [中国日报网](https://cn.chinadaily.com.cn/)                           | ✔️        | ✔️       | [chinadaily.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/chinadaily.py)       |
|                                                        | DuxiaoshiVideoClient                  | 度小视 (全民小视频)                | ✔️        | ✔️       | [duxiaoshi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/duxiaoshi.py)         |
|                                                        | DouyinVideoClient                     | 抖音视频                           | ✔️        | ✔️       | [douyin.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/douyin.py)               |
|                                                        | DongchediVideoClient                  | 懂车帝                             | ✔️        | ✔️       | [dongchedi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/dongchedi.py)         |
|                                                        | EyepetizerVideoClient                 | 开眼视频                           | ✔️        | ✔️       | [eyepetizer.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/eyepetizer.py)       |
|                                                        | [HaokanVideoClient](https://haokan.baidu.com/)                                                         | [好看视频](https://haokan.baidu.com/)                                                         | ✔️        | ✔️       | [haokan.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/haokan.py)               |
|                                                        | [HuyaVideoClient](https://www.huya.com/)                                                               | [虎牙视频](https://www.huya.com/)                                                             | ✔️        | ✔️       | [huya.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/huya.py)                   |
|                                                        | [IQiyiVideoClient](https://www.iqiyi.com/)                                                             | [爱奇艺](https://www.iqiyi.com/)                                                              | ✔️        | ✔️       | [iqiyi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/iqiyi.py)                 |
|                                                        | [Ku6VideoClient](https://www.ku6.com/)                                                                 | [酷6网](https://www.ku6.com/)                                                                 | ✔️        | ✔️       | [ku6.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ku6.py)                     |
|                                                        | [KuaishouVideoClient](https://www.kuaishou.com/)                                                       | [快手](https://www.kuaishou.com/)                                                             | ✔️        | ✔️       | [kuaishou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kuaishou.py)           |
|                                                        | [KugouMVVideoClient](https://www.kugou.com/mvweb/html/)                                                | [酷狗音乐MV](https://www.kugou.com/mvweb/html/)                                               | ✔️        | ✔️       | [kugoumv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kugoumv.py)             |
|                                                        | [KanKanNewsVideoClient](https://www.kankanews.com/)                                                    | [看看新闻](https://www.kankanews.com/)                                                        | ✔️        | ✔️       | [kankannews.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kankannews.py)       |
|                                                        | [LeshiVideoClient](https://www.le.com/)                                                                | [乐视视频](https://www.le.com/)                                                               | ✔️        | ✔️       | [leshi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/leshi.py)                 |
|                                                        | [MeipaiVideoClient](https://www.meipai.com/)                                                           | [美拍](https://www.meipai.com/)                                                               | ✔️        | ✔️       | [meipai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/meipai.py)               |
|                                                        | [MGTVVideoClient](https://www.mgtv.com/)                                                               | [芒果TV](https://www.mgtv.com/)                                                               | ✔️        | ✔️       | [mgtv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/mgtv.py)                   |
|                                                        | [M1905VideoClient](https://www.1905.com/)                                                              | [1905电影网](https://www.1905.com/)                                                           | ✔️        | ✔️       | [m1905.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/m1905.py)                 |
|                                                        | [OasisVideoClient](https://m.oasis.weibo.cn/v1/h5/share?uid=1642632024&luicode=10000012&lfid=hyhp_lz)  | [新浪绿洲](https://m.oasis.weibo.cn/v1/h5/share?uid=1642632024&luicode=10000012&lfid=hyhp_lz) | ✔️        | ✔️       | [oasis.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/oasis.py)                 |
|                                                        | [Open163VideoClient](https://open.163.com/)                                                            | [网易公开课](https://open.163.com/)                                                           | ✔️        | ✔️       | [open163.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/open163.py)             |
|                                                        | [PearVideoClient](https://www.pearvideo.com/)                                                          | [梨视频](https://www.pearvideo.com/)                                                          | ✔️        | ✔️       | [pear.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pear.py)                   |
|                                                        | [PipigaoxiaoVideoClient](https://www.pipigx.com/)                                                      | [皮皮搞笑](https://www.pipigx.com/)                                                           | ✔️        | ✔️       | [pipigaoxiao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipigaoxiao.py)     |
|                                                        | [PipixVideoClient](https://www.pipix.com/)                                                             | [皮皮虾](https://www.pipix.com/)                                                              | ✔️        | ✔️       | [pipix.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/pipix.py)                 |
|                                                        | [RednoteVideoClient](https://www.xiaohongshu.com/explore)                                              | [小红书](https://www.xiaohongshu.com/explore)                                                 | ✔️        | ✔️       | [rednote.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/rednote.py)             |
|                                                        | [SinaVideoClient](http://video.sina.com.cn/)                                                           | [新浪视频](http://video.sina.com.cn/)                                                         | ✔️        | ✔️       | [sina.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sina.py)                   |
|                                                        | [SixRoomVideoClient](https://v.6.cn/)                                                                  | [六间房视频](https://v.6.cn/)                                                                 | ✔️        | ✔️       | [sixroom.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sixroom.py)             |
|                                                        | [SohuVideoClient](https://tv.sohu.com/)                                                                | [搜狐视频](https://tv.sohu.com/)                                                              | ✔️        | ✔️       | [sohu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/sohu.py)                   |
|                                                        | [TencentVideoClient](https://v.qq.com/)                                                                | [腾讯视频](https://v.qq.com/)                                                                 | ✔️        | ✔️       | [tencent.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/tencent.py)             |
|                                                        | [WeiboVideoClient](https://weibo.com)                                                                  | [微博视频](https://weibo.com)                                                                 | ✔️        | ✔️       | [weibo.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/weibo.py)                 |
|                                                        | [WeishiVideoClient](https://isee.weishi.qq.com/)                                                       | [微视](https://isee.weishi.qq.com/)                                                           | ✔️        | ✔️       | [weishi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/weishi.py)               |
|                                                        | [WeSingVideoClient](https://kg.qq.com/index-pc.html)                                                   | [全民K歌](https://kg.qq.com/index-pc.html)                                                    | ✔️        | ✔️       | [wesing.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wesing.py)               |
|                                                        | [XiguaVideoClient](https://www.ixigua.com/)                                                            | [西瓜视频](https://www.ixigua.com/)                                                           | ✔️        | ✔️       | [xigua.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xigua.py)                 |
|                                                        | [XinpianchangVideoClient](https://www.xinpianchang.com/)                                               | [新片场](https://www.xinpianchang.com/)                                                       | ✔️        | ✔️       | [xinpianchang.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xinpianchang.py)   |
|                                                        | [XuexiCNVideoClient](https://www.xuexi.cn/)                                                            | [学习强国](https://www.xuexi.cn/)                                                             | ✔️        | ✔️       | [xuexicn.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/xuexicn.py)             |
|                                                        | [YoukuVideoClient](https://www.youku.com/)                                                             | [优酷视频](https://www.youku.com/)                                                            | ✔️        | ✔️       | [youku.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youku.py)                 |
|                                                        | [YinyuetaiVideoClient](https://www.yinyuetai.com/)                                                     | [音悦台 (关停ing)](https://www.yinyuetai.com/)                                                | ✔️        | ✔️       | [yinyuetai.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/yinyuetai.py)         |
|                                                        | [ZhihuVideoClient](https://www.zhihu.com/)                                                             | [知乎视频](https://www.zhihu.com/)                                                            | ✔️        | ✔️       | [zhihu.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zhihu.py)                 |
|                                                        | [ZuiyouVideoClient](https://share.xiaochuankeji.cn/home)                                               | [最右](https://share.xiaochuankeji.cn/home)                                                   | ✔️        | ✔️       | [zuiyou.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/zuiyou.py)               |
| **Overseas Platforms**                                 | [ArteTVVideoClient](https://www.arte.tv/en/)                                                           | [德法公共电视网](https://www.arte.tv/en/)                                                     | ✔️        | ✔️       | [artetv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/artetv.py)               |
|                                                        | [ABCVideoClient](https://www.abc.net.au/)                                                              | [澳大利亚广播公司](https://www.abc.net.au/)                                                   | ✔️        | ✔️       | [abc.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/abc.py)                     |
|                                                        | [BeaconVideoClient](https://beacon.tv/)                                                                | [BeaconTV](https://beacon.tv/)                                                                | ✔️        | ✔️       | [beacon.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/beacon.py)               |
|                                                        | [CCCVideoClient](https://media.ccc.de/)                                                                | [CCC视频 (黑客大会视频)](https://media.ccc.de/)                                               | ✔️        | ✔️       | [ccc.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ccc.py)                     |
|                                                        | [FoxNewsVideoClient](https://www.foxnews.com/)                                                         | [福克斯新闻](https://www.foxnews.com/)                                                        | ✔️        | ✔️       | [foxnews.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/foxnews.py)             |
|                                                        | [GeniusVideoClient](https://genius.com/)                                                               | [Rap Genius (嘻哈百科)](https://genius.com/)                                                  | ✔️        | ✔️       | [genius.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/genius.py)               |
|                                                        | [KakaoVideoClient](https://tv.kakao.com/)                                                              | [KakaoTV](https://tv.kakao.com/)                                                              | ✔️        | ✔️       | [kakao.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/kakao.py)                 |
|                                                        | [NuVidVideoClient](https://www.nuvid.com/)                                                             | [NuVid.com](https://www.nuvid.com/)                                                           | ✔️        | ✔️       | [nuvid.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/nuvid.py)                 |
|                                                        | [PlusFIFAVideoClient](https://www.plus.fifa.com/en/?gl=us)                                             | [FIFA+平台 (国际足联+)](https://www.plus.fifa.com/en/?gl=us)                                  | ✔️        | ✔️       | [plusfifa.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/plusfifa.py)           |
|                                                        | [PlayerPLVideoClient](https://player.pl/international)                                                 | [Player.pl (波兰流行视频点播站)](https://player.pl/international)                             | ✔️        | ✔️       | [playerpl.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/playerpl.py)           |
|                                                        | [RedditVideoClient](https://www.reddit.com/)                                                           | [红迪网](https://www.reddit.com/)                                                             | ✔️        | ✔️       | [reddit.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/reddit.py)               |
|                                                        | [TBNUKVideoClient](https://watch.tbn.uk/)                                                              | [英国三一电视台点播网站](https://watch.tbn.uk/)                                               | ✔️        | ✔️       | [tbnuk.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/tbnuk.py)                 |
|                                                        | [TedVideoClient](https://www.ted.com/)                                                                 | [TED视频](https://www.ted.com/)                                                               | ✔️        | ✔️       | [ted.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/ted.py)                     |
|                                                        | [UnityVideoClient](https://unity.com/)                                                                 | [Unity](https://unity.com/)                                                                   | ✔️        | ✔️       | [unity.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/unity.py)                 |
|                                                        | [WWEVideoClient](https://www.wwe.com/)                                                                 | [世界摔角娱乐](https://www.wwe.com/)                                                          | ✔️        | ✔️       | [wwe.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wwe.py)                     |
|                                                        | [WittyTVVideoClient](https://www.wittytv.it/)                                                          | [Witty TV (意大利多媒体娱乐平台)](https://www.wittytv.it/)                                    | ✔️        | ✔️       | [wittytv.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/wittytv.py)             |
|                                                        | [YouTubeVideoClient](https://www.youtube.com/)                                                         | [油管视频](https://www.youtube.com/)                                                          | ✔️        | ✔️       | [youtube.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/sources/youtube.py)             |

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
| [JXM3U8VideoClient](https://jx.m3u8.tv/jiexi/?url=)               | [M3U8.TV解析](https://jx.m3u8.tv/jiexi/?url=)                           |   ✔️     |   ✔️     | [jxm3u8.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/jxm3u8.py)         |
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
| [SpapiVideoClient](https://api.spapi.cn/)                         | [短视频-去水印解析下载](https://api.spapi.cn/)                          |   ✔️     |   ✔️     | [spapi.py](https://github.com/CharlesPikachu/videodl/blob/master/videodl/modules/common/spapi.py)           |
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

- **[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)**: FFmpeg is a general-purpose media tool that can download standard HLS/m3u8 streams, but it assumes that the playlist and segment URLs strictly follow the protocol. 
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

- **[Bento4](https://www.bento4.com/)**: Bento4 is an open-source MP4/DASH/HLS/CMAF toolkit, and in the N_m3u8DL-RE ecosystem it is mainly related as the source of auxiliary utilities such as "mp4decrypt" for handling certain packaged media workflows.
  Therefore, when using N_m3u8DL-RE to handle some packaged media workflows that involve encryption (*e.g.*, `TBNUKVideoClient`, `PlayerPLVideoClient` and `PlusFIFAVideoClient`), you need to make sure the Bento4 tools are available in your runtime environment.
  A quick way to verify Bento4 is that you should be able to run
  ```bash
  mp4decrypt --version
  ```
  If it returns the version information successfully, Bento4 is installed correctly, otherwise the installation has failed or the tool is not in your `PATH`.

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

This guide shows the fastest ways to use videodl from the command line and from Python.

videodl supports two common workflows:

1. Parse and download in one step
2. Parse first, inspect the result, then download

#### Quick Use Videodl from Command Line

(1) Download a video from a URL

```bash
videodl -i "https://www.acfun.cn/v/ac36491489"
```

If videodl can find a matching client, it will parse the URL and start downloading automatically.

The demonstration is as follows,

<div align="center">
  <img src="https://github.com/CharlesPikachu/videodl/raw/master/docs/screenshot.gif" width="600"/>
</div>
<br />

(2) Start interactive mode

If `-i` is not provided, videodl starts in terminal mode:

```bash
videodl
```

Then enter a video URL when prompted. In interactive mode:

- enter `q` to quit
- enter `r` to restart the UI


(3) Restrict parsing to specific clients

If the URL belongs to a known platform, specifying the client is usually faster.

```bash
videodl -i "https://www.acfun.cn/v/ac36491489" -a "AcFunVideoClient"
```

You can also provide multiple clients:

```bash
videodl -i "URL" -a "AcFunVideoClient,BilibiliVideoClient"
```

(4) Use only common / generic parsers

```bash
videodl -i "URL" -g
```

This is equivalent to `apply_common_video_clients_only=True` in Python.

(5) Set client config from the command line

Some options are passed as JSON strings.

Example: change the output directory for one client:

```bash
videodl -i "https://www.acfun.cn/v/ac36491489" \
  -a "AcFunVideoClient" \
  -c '{"AcFunVideoClient": {"work_dir": "downloads"}}'
```

Example: pass custom headers or proxies:

```bash
videodl -i "URL" \
  -r '{"AcFunVideoClient": {"headers": {"User-Agent": "Mozilla/5.0"}, "proxies": {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}}}'
```

(6) CLI options

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

#### Recommended Parsing Commands for Common Streaming Platforms

Recommended parsing and downloading commands for some widely used video platforms are as follows,

```bash
# IQIYI / YOUKU / TENCENT / PPTV / MGTV / CCTV / BILIBILI (爱奇艺, 优酷, 腾讯视频, PPTV, 芒果TV, CCTV, B站等平台的电影电视剧)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a IM1907VideoClient (Recommended, 1080p)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a SENJiexiVideoClient (Recommended)
videodl -i "IQIYI/YOUKU/TENCENT/PPTV/MGTV/CCTV/BILIBILI VIDEO URL" -g -a JXM3U8VideoClient
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
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a SpapiVideoClient
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

#### Quick Use Videodl from Python

(1) Create a `VideoClient`

```python
from videodl import videodl

video_client = videodl.VideoClient()
```

This creates a high-level client that can:

- choose a suitable parser
- parse a URL into one or more `VideoInfo` objects
- download the parsed videos

(2) Parse and download in one step

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://www.acfun.cn/v/ac36491489")
video_client.download(video_infos)
```

(3) Start interactive mode from Python

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_client.startparseurlcmdui()
```

(4) Use only selected clients

```python
from videodl import videodl

video_client = videodl.VideoClient(
    allowed_video_sources=["AcFunVideoClient"]
)
video_infos = video_client.parsefromurl("https://www.acfun.cn/v/ac36491489")
video_client.download(video_infos)
```

(5) Use only common / generic clients

```python
from videodl import videodl

video_client = videodl.VideoClient(apply_common_video_clients_only=True)
video_infos = video_client.parsefromurl("URL")
video_client.download(video_infos)
```

#### Parse First, Then Inspect the Result

Sometimes it is useful to inspect the parsed result before downloading.

```python
from videodl import videodl

video_client = videodl.VideoClient(allowed_video_sources=["AcFunVideoClient"])
video_infos = video_client.parsefromurl("https://www.acfun.cn/v/ac36491489")

for info in video_infos:
    print(info["source"])
    print(info["title"])
    print(info["download_url"])
    print(info["save_path"])
    print(info["ext"])
    print(info["err_msg"])
```

A parsed item is a `VideoInfo` object. It behaves like both a dataclass object and a dictionary.

For example, both styles work:

```python
info = video_infos[0]
print(info.title)
print(info["title"])
```

Common fields include:

- `source`: which client produced this result
- `title`: video title
- `download_url`: resolved media URL
- `save_path`: output file path
- `ext`: file extension
- `err_msg`: parsing error, if any
- `download_with_ffmpeg`: whether ffmpeg should be used
- `download_with_aria2c`: whether aria2c should be used
- `enable_nm3u8dlre`: whether N_m3u8DL-RE should be used

#### Download a Parsed Result Later

Once `video_infos` is ready, download it like this:

```python
video_client.download(video_infos)
```

You can also modify the parsed result before downloading.

Example: enable `aria2c` for a direct file download:

```python
for info in video_infos:
    info["download_with_aria2c"] = True

video_client.download(video_infos)
```

Example: enable `N_m3u8DL-RE` for HLS / m3u8 downloads:

```python
for info in video_infos:
    info["enable_nm3u8dlre"] = True

video_client.download(video_infos)
```

Example: force `ffmpeg` download:

```python
for info in video_infos:
    info["download_with_ffmpeg"] = True

video_client.download(video_infos)
```

#### Common Configuration Examples

(1) Change the output directory

```python
from videodl import videodl

video_client = videodl.VideoClient(
    init_video_clients_cfg={
        "AcFunVideoClient": {
            "work_dir": "downloads"
        }
    },
    allowed_video_sources=["AcFunVideoClient"]
)
```

(2) Pass cookies for parsing or downloading

```python
from videodl import videodl

cookies = "your cookies here"

video_client = videodl.VideoClient(
    init_video_clients_cfg={
        "SomeVideoClient": {
            "default_parse_cookies": cookies,
            "default_download_cookies": cookies,
        }
    },
    allowed_video_sources=["SomeVideoClient"]
)
```

(3) Pass custom request options

`requests_overrides` is useful when a client needs extra headers, cookies, timeout settings, or proxies.

```python
from videodl import videodl

video_client = videodl.VideoClient(
    requests_overrides={
        "AcFunVideoClient": {
            "headers": {
                "User-Agent": "Mozilla/5.0"
            },
            "proxies": {
                "http": "http://127.0.0.1:7890",
                "https": "http://127.0.0.1:7890"
            }
        }
    },
    allowed_video_sources=["AcFunVideoClient"]
)
```

(4) Set download threads per client

```python
from videodl import videodl

video_client = videodl.VideoClient(
    clients_threadings={
        "AcFunVideoClient": 8
    },
    allowed_video_sources=["AcFunVideoClient"]
)
```

#### Direct Media URLs

If the input URL is already a direct media link, videodl will try to handle it directly without needing a platform-specific / general-purpose video client as a parser.

```python
from videodl import videodl

video_client = videodl.VideoClient()
video_infos = video_client.parsefromurl("https://example.com/video.mp4")
video_client.download(video_infos)
```

#### Tips

(1) Prefer specific clients when possible

This is usually faster:

```python
video_client = videodl.VideoClient(allowed_video_sources=["AcFunVideoClient"])
```

than searching through all supported clients.

(2) Generic parsers are useful when platform-specific parsing does not work

Use:

```python
videodl.VideoClient(apply_common_video_clients_only=True)
```

or on the CLI:

```bash
videodl -g -i "URL"
```

(3) Some download accelerators require external tools

Depending on how a video is parsed, videodl may work with:

- `ffmpeg`
- `aria2c`
- `N_m3u8DL-RE`

Make sure they are installed and available in your environment before enabling them.


(4) A parse result may contain multiple videos

Some URLs may return more than one `VideoInfo`, so always treat the return value of `parsefromurl()` as a list.

Please refer to the documentation for further details: https://videofetch.readthedocs.io/


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