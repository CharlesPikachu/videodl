# Quick Start

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
