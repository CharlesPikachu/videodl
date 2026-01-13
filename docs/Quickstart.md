# Quick Start

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
# IQIYI / YOUKU / TENCENT (爱奇艺, 优酷, 腾讯视频, 含VIP)
videodl -i "IQIYI/YOUKU/TENCENT VIDEO URL" -g -a XMFlvVideoClient
videodl -i "IQIYI/YOUKU/TENCENT VIDEO URL" -g -a GVVIPVideoClient
# Examples
videodl -i "https://www.iqiyi.com/v_cy4phe8b08.html" -g -a XMFlvVideoClient
videodl -i "https://v.qq.com/x/cover/mzc002001nl46xm/t410130yz0y.html" -g -a XMFlvVideoClient

# MIGU (咪咕视频)
videodl -i "MIGU VIDEO URL" -g -a RayVideoClient
videodl -i "MIGU VIDEO URL" -g -a KedouVideoClient
# Examples
videodl -i "https://www.miguvideo.com/p/detail/759959727" -g -a KedouVideoClient

# DOUYIN / TIKTOK / KUAISHOU / XIAOHONGSHU / YOUTUBE / FACEBOOK / TITTER (X) (抖音, 抖音海外, 快手, 小红书, 油管, 脸书, 推特视频等)
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a VideoFKVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a SnapAnyVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a IIILabVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a VgetVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a SnapWCVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a KedouVideoClient
videodl -i "DOUYIN/TIKTOK/KUAISHOU/XIAOHONGSHU/YOUTUBE/FACEBOOK/TITTER VIDEO URL" -g -a KuKuToolVideoClient
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
    "download_with_ffmpeg_cctv": false,
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
For example, for an IQIYI/YOUKU/TENCENT VIDEO URL, you can run the following command,

```bash
videodl -i "IQIYI/YOUKU/TENCENT VIDEO URL" -g -a XMFlvVideoClient
videodl -i "IQIYI/YOUKU/TENCENT VIDEO URL" -g -a GVVIPVideoClient
```

Of course, it’s worth noting that this approach may come with some drawbacks, for example, some third-party parsing services may occasionally insert a few seconds of unwanted ads into the downloaded video.

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
