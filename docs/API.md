# Videodl APIs

This document describes the main public APIs for working with video parsing and downloading in videodl.

It focuses on three parts:

- `VideoClient`: the main high-level entry point.
- `BaseVideoClient`: the base class used by site-specific clients.
- `VideoInfo`: the result object returned by parsing and downloading methods.


## `VideoClient`

`VideoClient` is the main class for external use.

It manages multiple video backends, chooses the right parser for a URL, and dispatches downloads to the correct client automatically.

Module path:

`videodl.videodl.VideoClient`

Constructor:

```python
VideoClient(
    allowed_video_sources: list | None = None,
    init_video_clients_cfg: dict | None = None,
    clients_threadings: dict | None = None,
    requests_overrides: dict | None = None,
    apply_common_video_clients_only: bool = False,
)
```

Arguments:

- **`allowed_video_sources`**
  
  A list of enabled client names.
  - If this is `None` or empty, `VideoClient` enables all registered clients.
  - Each item should be a client name such as `"AcFunVideoClient"`.
  
  Example:
  ```python
  allowed_video_sources = ["AcFunVideoClient"]
  ```

- **`init_video_clients_cfg`**

  Per-client initialization settings.
  - The key is the client name.
  - The value is a dictionary of constructor arguments passed to that client.
  - This is useful when different sources need different work directories, cookies, retry settings, or proxy behavior.
  
  Common options include:
  - `work_dir`
  - `auto_set_proxies`
  - `random_update_ua`
  - `max_retries`
  - `maintain_session`
  - `disable_print`
  - `freeproxy_settings`
  - `default_search_cookies`
  - `default_download_cookies`
  - `default_parse_cookies`

  Advanced options supported by `BaseVideoClient` can also be passed here, for example:
  - `enable_parse_curl_cffi`
  - `enable_search_curl_cffi`
  - `enable_download_curl_cffi`

  Example:
  ```python
  init_video_clients_cfg = {
      "SohuVideoClient": {
          "work_dir": "downloads/sohu",
          "max_retries": 3,
          "maintain_session": True,
      }
  }
  ```

- **`clients_threadings`**

  Per-client download thread counts.
  - The key is the client name.
  - The value is the number of download threads for that source.
  - If a source is not included, `5` is used by default.

  Example:
  ```python
  clients_threadings = {
      "XinpianchangVideoClient": 3,
  }
  ```

- **`requests_overrides`**
  
  Per-client request settings used during parsing and downloading.
  
  Typical fields are:
  - `headers`
  - `cookies`
  - `proxies`
  
  Example:
  ```python
  requests_overrides = {
      "TencentVideoClient": {
          "headers": {"User-Agent": "Mozilla/5.0"},
          "cookies": {"sessionid": "example"}
      }
  }
  ```

- **`apply_common_video_clients_only`**
  
  Whether to use only the generic parsers.
  - `False`: try platform-specific clients first, then generic parsers if needed.
  - `True`: skip platform-specific clients and use only common parsers.
  
  This can be useful when the target URL is not from a built-in supported site.

#### `VideoClient.parsefromurl()`

Parse a video URL and return one or more `VideoInfo` objects.

```python
VideoClient.parsefromurl(url: str) -> list[VideoInfo]
```

Parsing behavior:

When `VideoClient.parsefromurl()` is called, `VideoClient` uses the following strategy:

1. Check whether the URL looks like a direct media link.
2. If not, try platform-specific clients, unless `apply_common_video_clients_only=True`.
3. If still no valid result is found, try generic parsers.
4. If needed, fall back to the web media grabber.

This logic is internal. In normal use, only a URL needs to be provided.

A single URL may return:

- one item for a normal video,
- multiple items for multi-part content,
- or an empty result if parsing fails.

Example:

```python
from videodl.videodl import VideoClient

client = VideoClient(
    allowed_video_sources=["AcFunVideoClient"],
    requests_overrides={
        "AcFunVideoClient": {
            "headers": {"User-Agent": "Mozilla/5.0"}
        }
    }
)

video_infos = client.parsefromurl("https://www.acfun.cn/v/ac123456")

for info in video_infos:
    print(info.title)
    print(info.source)
    print(info.download_url)
    print(info.save_path)
```

#### `VideoClient.download()`

Download parsed videos.

```python
VideoClient.download(video_infos: list[VideoInfo]) -> list[VideoInfo]
```

`VideoClient` automatically groups items by `source` and sends them to the correct underlying client.

Notes:

- `video_infos` should usually be the output of `VideoClient.parsefromurl()`.
- Thread counts come from `clients_threadings`.
- Request settings come from `requests_overrides`.

Example:

```python
video_infos = client.parsefromurl("https://www.acfun.cn/v/ac123456")
client.download(video_infos)
```

#### `VideoClient.startparseurlcmdui()`

Start the interactive terminal UI.

```python
VideoClient.startparseurlcmdui() -> None
```

In this mode, the program repeatedly asks for a video URL, parses it, and downloads the result.

Special inputs:

- `q`: quit
- `r`: restart

This is mainly for command-line use.


## `BaseVideoClient`

`BaseVideoClient` is the base class for all site-specific clients.

Module path:

`videodl.modules.sources.BaseVideoClient`

Examples of subclasses include clients such as,

- `videodl.modules.sources.ABCVideoClient`
- `videodl.modules.sources.AcFunVideoClient`
- `videodl.modules.sources.ArteTVVideoClient`
- `videodl.modules.sources.BaiduTiebaVideoClient`
- `videodl.modules.sources.BeaconVideoClient`
- `videodl.modules.sources.BilibiliVideoClient`
- `videodl.modules.sources.C56VideoClient`
- `videodl.modules.sources.CCCVideoClient`
- `videodl.modules.sources.CCTVVideoClient`
- `videodl.modules.sources.CCtalkVideoClient`
- `videodl.modules.sources.DongchediVideoClient`
- `videodl.modules.sources.DouyinVideoClient`
- `videodl.modules.sources.DuxiaoshiVideoClient`
- `videodl.modules.sources.EyepetizerVideoClient`
- `videodl.modules.sources.FoxNewsVideoClient`
- `videodl.modules.sources.GeniusVideoClient`
- `videodl.modules.sources.HaokanVideoClient`
- `videodl.modules.sources.HuyaVideoClient`
- `videodl.modules.sources.IQiyiVideoClient`
- `videodl.modules.sources.KakaoVideoClient`
- `videodl.modules.sources.KanKanNewsVideoClient`
- `videodl.modules.sources.Ku6VideoClient`
- `videodl.modules.sources.KuaishouVideoClient`
- `videodl.modules.sources.KugouMVVideoClient`
- `videodl.modules.sources.LeshiVideoClient`
- `videodl.modules.sources.M1905VideoClient`
- `videodl.modules.sources.MGTVVideoClient`
- `videodl.modules.sources.MeipaiVideoClient`
- `videodl.modules.sources.OasisVideoClient`
- `videodl.modules.sources.Open163VideoClient`
- `videodl.modules.sources.PearVideoClient`
- `videodl.modules.sources.PipigaoxiaoVideoClient`
- `videodl.modules.sources.PipixVideoClient`
- `videodl.modules.sources.PlayerPLVideoClient`
- `videodl.modules.sources.PlusFIFAVideoClient`
- `videodl.modules.sources.RedditVideoClient`
- `videodl.modules.sources.RednoteVideoClient`
- `videodl.modules.sources.SinaVideoClient`
- `videodl.modules.sources.SixRoomVideoClient`
- `videodl.modules.sources.SohuVideoClient`
- `videodl.modules.sources.TBNUKVideoClient`
- `videodl.modules.sources.TedVideoClient`
- `videodl.modules.sources.TencentVideoClient`
- `videodl.modules.sources.UnityVideoClient`
- `videodl.modules.sources.WWEVideoClient`
- `videodl.modules.sources.WeSingVideoClient`
- `videodl.modules.sources.WeiboVideoClient`
- `videodl.modules.sources.WeishiVideoClient`
- `videodl.modules.sources.WittyTVVideoClient`
- `videodl.modules.sources.XiguaVideoClient`
- `videodl.modules.sources.XinpianchangVideoClient`
- `videodl.modules.sources.XuexiCNVideoClient`
- `videodl.modules.sources.YinyuetaiVideoClient`
- `videodl.modules.sources.YoukuVideoClient`
- `videodl.modules.sources.YouTubeVideoClient`
- `videodl.modules.sources.ZhihuVideoClient`
- `videodl.modules.sources.ZuiyouVideoClient`
- ...
- `videodl.modules.common.AnyFetcherVideoClient`
- `videodl.modules.common.BVVideoClient`
- `videodl.modules.common.BugPkVideoClient`
- `videodl.modules.common.GVVIPVideoClient`
- `videodl.modules.common.GVVideoClient`
- `videodl.modules.common.IIILabVideoClient`
- `videodl.modules.common.IM1907VideoClient`
- `videodl.modules.common.JXM3U8VideoClient`
- `videodl.modules.common.KIT9VideoClient`
- `videodl.modules.common.KedouVideoClient`
- `videodl.modules.common.KuKuToolVideoClient`
- `videodl.modules.common.LongZhuVideoClient`
- `videodl.modules.common.LvlongVideoClient`
- `videodl.modules.common.MiZhiVideoClient`
- `videodl.modules.common.NoLogoVideoClient`
- `videodl.modules.common.ODwonVideoClient`
- `videodl.modules.common.PVVideoClient`
- `videodl.modules.common.QZXDPToolsVideoClient`
- `videodl.modules.common.QingtingVideoClient`
- `videodl.modules.common.QwkunsVideoClient`
- `videodl.modules.common.RayVideoClient`
- `videodl.modules.common.SENJiexiVideoClient`
- `videodl.modules.common.SnapAnyVideoClient`
- `videodl.modules.common.SnapWCVideoClient`
- `videodl.modules.common.SpapiVideoClient`
- `videodl.modules.common.VgetVideoClient`
- `videodl.modules.common.VideoFKVideoClient`
- `videodl.modules.common.WoofVideoClient`
- `videodl.modules.common.XCVTSVideoClient`
- `videodl.modules.common.XMFlvVideoClient`
- `videodl.modules.common.XZDXVideoClient`
- `videodl.modules.common.XiaolvfangVideoClient`
- `videodl.modules.common.XiazaitoolVideoClient`
- `videodl.modules.common.ZanqianbaVideoClient`
- ...

In most cases, external users do not create `BaseVideoClient` directly. Instead, they either:

- use `VideoClient`, or
- use a concrete subclass built on top of `BaseVideoClient`.

Constructor:

```python
BaseVideoClient(
    auto_set_proxies: bool = False,
    random_update_ua: bool = False,
    enable_parse_curl_cffi: bool = False,
    enable_search_curl_cffi: bool = False,
    enable_download_curl_cffi: bool = False,
    max_retries: int = 5,
    maintain_session: bool = False,
    logger_handle = None,
    disable_print: bool = False,
    work_dir: str = "videodl_outputs",
    freeproxy_settings: dict | None = None,
    default_search_cookies: dict | None = None,
    default_download_cookies: dict | None = None,
    default_parse_cookies: dict | None = None,
)
```

Arguments:

- **`auto_set_proxies`**
  
  Automatically fetch and apply proxies for requests.
  Use this when a source frequently blocks direct requests.

- **`random_update_ua`**

  Randomly refresh the `User-Agent` when a new session is created.
  This can help reduce repeated identical requests.

- **`enable_parse_curl_cffi`**

  Use `curl_cffi` sessions instead of normal `requests` sessions for parsing.
  This option is useful for some sites with stricter request checks.

- **`enable_search_curl_cffi`**

  Use `curl_cffi` sessions instead of normal `requests` sessions for searching.
  This option is useful for some sites with stricter request checks.

- **`enable_download_curl_cffi`**

  Use `curl_cffi` sessions instead of normal `requests` sessions for downloading.
  This option is useful for some sites with stricter request checks.

- **`max_retries`**

  Maximum number of retries for HTTP requests.

- **`maintain_session`**

  Whether to reuse the same HTTP session across requests.
  - `False`: recreate the session more often.
  - `True`: keep cookies and session state between requests.

- **`logger_handle`**

  Optional logger instance.
  If not provided, a default logger is created.

- **`disable_print`**

  Whether to suppress console output.

- **`work_dir`**

  Root directory for outputs.

- **`freeproxy_settings`**

  Optional settings for the proxy client used when `auto_set_proxies=True`.

- **`default_search_cookies`**

  Default cookies used for search.
  This is helpful for sites that require login cookies or other session information.

- **`default_download_cookies`**

  Default cookies used for download.
  This is helpful for sites that require login cookies or other session information.

- **`default_parse_cookies`**

  Default cookies used for parse.
  This is helpful for sites that require login cookies or other session information.

#### `BaseVideoClient.parsefromurl()`

Parse a URL and return `VideoInfo` objects.

```python
BaseVideoClient.parsefromurl(url: str, request_overrides: dict | None = None) -> list[VideoInfo]
```

This method is defined by subclasses. `BaseVideoClient` itself only provides the interface.

`request_overrides` usually contains request-related fields such as:

- `headers`
- `cookies`
- `proxies`

Each returned `VideoInfo` should normally include at least:

- `source`
- `download_url`
- `save_path`

A typical subclass may also fill fields such as:

- `title`
- `identifier`
- `cover_url`
- `raw_data`
- `err_msg`

Example:

```python
video_infos = some_client.parsefromurl(
    "https://example.com/video/123",
    request_overrides={
        "headers": {"User-Agent": "Mozilla/5.0"},
        "cookies": {"sessionid": "example"},
    },
)
```

#### `BaseVideoClient.download()`

Download one or more videos.

```python
BaseVideoClient.download(
    video_infos: list[VideoInfo],
    num_threadings: int = 5,
    request_overrides: dict | None = None,
) -> list[VideoInfo]
```

This method handles concurrency and chooses the actual download strategy automatically.

Depending on the data in each `VideoInfo`, the downloader may use:

- normal HTTP download,
- `ffmpeg`,
- `N_m3u8DL-RE`,
- `aria2c`,
- separate video/audio download followed by merge.

Returns:

- a list of successfully downloaded `VideoInfo` objects.

Example:

```python
downloaded = some_client.download(video_infos, num_threadings=3)

for item in downloaded:
    print(item.save_path)
```

#### `BaseVideoClient.belongto()`

Check whether a URL belongs to a given source.

```python
BaseVideoClient.belongto(url: str, valid_domains: list[str] | set[str] | None = None) -> bool
```

This is mainly a helper for client implementations, but it can also be useful when building custom routing logic.

Example:

```python
BaseVideoClient.belongto(
    "https://www.acfun.cn/v/ac123456",
    valid_domains={"acfun.cn"},
)
# True
```

#### Request helpers for subclass implementations

`BaseVideoClient` also provides retry-enabled request helpers:

- `get(url, **kwargs)`
- `post(url, **kwargs)`

These methods are mainly intended for subclass authors, not for normal end users.


## `VideoInfo`

`VideoInfo` is the core data object returned by parsing methods and consumed by download methods.

It behaves like both:

- an object, for example `info.title`,
- and a dictionary, for example `info["title"]`.

Common fields:

- `source`: client name, such as `"AcFunVideoClient"`
- `title`: video title
- `cover_url`: cover image URL if available
- `raw_data`: original parsed data
- `err_msg`: error message if parsing failed
- `identifier`: unique ID for the video
- `download_url`: main video download URL or local intermediate file
- `save_path`: output file path
- `ext`: output file extension
- `default_download_headers`: optional per-item headers
- `default_download_cookies`: optional per-item cookies
- `audio_download_url`
- `audio_save_path`
- `audio_ext`
- `default_audio_download_headers`
- `default_audio_download_cookies`
- `download_with_ffmpeg`
- `enable_nm3u8dlre`
- `download_with_aria2c`
- `ffmpeg_settings`
- `nm3u8dlre_settings`
- `aria2c_settings`

Useful properties:

- **`with_valid_download_url`**:

  Returns `True` when the main download URL is valid.

- **`with_valid_audio_download_url`**

  Returns `True` when the audio download URL is valid.

Example:

```python
{
    "source": "AcFunVideoClient",
    "title": "Example Video",
    "download_url": "https://example.com/video.m3u8",
    "save_path": "videodl_outputs/AcFunVideoClient/Example Video.mp4",
    "ext": "mp4",
    "identifier": "ac123456"
}
```

