# Quick Start

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
# DOUYIN / TIKTOK / KUAISHOU / XIAOHONGSHU (抖音, 抖音海外, 快手, 小红书等短视频)
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a SnapWCVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a KedouVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a KuKuToolVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a NoLogoVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU VIDEO URL" -g -a IIILabVideoClient
...
# CCTV (央视网)
videodl -i "CCTV VIDEO URL" -a CCTVVideoClient
# YOUTUBE (油管)
videodl -i "YOUTUBE VIDEO URL" -a YouTubeVideoClient
# BILIBILI (B站)
videodl -i "BILIBILI VIDEO URL" -a BilibiliVideoClient
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
