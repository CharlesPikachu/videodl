# Videodl APIs


## `videodl.videodl.VideoClient`

The `VideoClient` class is a high-level manager for multiple site-specific video download clients. It:

- Initializes one internal client per video source.
- Parses video information from a given URL.
- Dispatches download jobs with configurable threading and request overrides.
- Optionally provides an interactive command-line UI.

`VideoClient()` accept the following arguments,

- **allowed_video_sources**: `list[str] | None`  
  List of video source names to enable (*e.g.* `["YouTubeVideoClient"`, `"ZhihuVideoClient"]`).  
  - If `None` or empty, it defaults to **all** sources registered in `VideoClientBuilder.REGISTERED_MODULES` and `CommonVideoClientBuilder.REGISTERED_MODULES`.
  - Each entry must correspond to a valid backend module.

- **init_video_clients_cfg**: `dict[str, dict] | None`  
  Per-source configuration overrides for initializing each underlying video client.  
  - Key: source name (*e.g.* `"YouTubeVideoClient"`).  
  - Value: a `dict` of configuration options that will update the default config.  
  - Default base config for every client:

    - `auto_set_proxies`: `False`  
    - `random_update_ua`: `False`  
    - `max_retries`: `5`  
    - `maintain_session`: `False`  
    - `logger_handle`: internal `LoggerHandle` instance  
    - `disable_print`: `False`  
    - `work_dir`: `'videodl_outputs'`  
    - `proxy_sources`: `None`  
    - `default_search_cookies`: `{}`  
    - `default_download_cookies`: `{}`  
    - `default_parse_cookies`: `{}`  
    - `type`: set automatically to the current `allowed_video_source`
  - Example: override work directory and enable proxy for `YouTubeVideoClient`
  
        init_video_clients_cfg = {
            "YouTubeVideoClient": {
                "work_dir": "outputs/youtube",
                "auto_set_proxies": True
            }
        }

- **clients_threadings**: `dict[str, int] | None`  
  Per-source number of download threads.  
  - Key: source name.  
  - Value: number of worker threads when downloading from that source.  
  - If a source is missing in this dict, `download` will default to `5` threads for that source.

  - Example:

        clients_threadings = {
            "YouTubeVideoClient": 8,
            "ZhihuVideoClient": 4
        }

- **requests_overrides**: `dict[str, dict] | None`  
  Per-source overrides for HTTP request options (headers, cookies, proxies, etc.).  
  - Used in both `parsefromurl` and `download` for that specific source.
  - Key: source name.  
  - Value: a `dict` passed as `request_overrides` to the underlying client.

  - Example:

        requests_overrides = {
            "YouTubeVideoClient": {
                "headers": {"User-Agent": "MyCustomUA/1.0"},
                "proxies": {"https": "http://127.0.0.1:7890"}
            }
        }

- **apply_common_video_clients_only**: `bool`  
  Starting from videofetch 0.3.0, we introduced a generic parser interface. 
  The default parsing order is to first use the parsers in the supported list; 
  if all of them fail, the generic parsers are then invoked one by one until parsing succeeds. 
  If you know your video is not in the supported list, you can set `apply_common_video_clients_only` to `True` to reduce parsing time.

#### `VideoClient.startparseurlcmdui`

Start an **interactive command-line UI** for parsing and downloading videos from URLs, the behavior can be described as

- Enters an infinite loop:
  1. Prints basic library info (version and work directories).
  2. Prompts the user:  
     `Please enter video url for downloading:`
  3. Reads user input via `processinputs`.
  4. Calls `parsefromurl` on that URL.
  5. Calls `download` on the parsed video infos.

- Special commands in the prompt:
  - Enter `q` (or `Q`): quit the program.
  - Enter `r` (or `R`): restart the UI loop.
  - Any other input is treated as a video URL.

#### `VideoClient.parsefromurl`

Parse video information from a given URL and choose the proper backend client automatically.

Arguments:

- **url**: `str`  
  The video page URL. It should belong to one of the `allowed_video_sources`. The method relies on each underlying client’s `belongto(url)` to detect ownership.

Return Values:

- A `list` of video information dicts. The exact structure depends on the underlying client implementation, but **each dict must at least contain a `source` field** matching one of the source names (*e.g.* `"YouTubeVideoClient"`, `"ZhihuVideoClient"`), which is used later by `download`.

  Typical fields may include (depending on implementation):

  - `source`: source name string.
  - `title`: video title.
  - `download_url`: actual download URL.
  - `raw_data`: raw data before parsing.
  - `file_path`: save path for each video.

#### `VideoClient.download`

Dispatch download tasks for a list of parsed video information items.

Arguments:

- **video_infos**: `list[dict]`  
  List of video info dicts, usually the output of `parsefromurl`.  
  Each dict must contain a `source` key that matches one of the initialized video clients.

Return Values:

- `None`


## `videodl.modules.sources.base.BaseVideoClient`

`BaseVideoClient` is the **base class** for all site-specific video downloaders in this library.

All concrete video clients (such as `YouTubeVideoClient`, `BilibiliVideoClient`, `CCTVVideoClient`, etc.) inherit from this class and reuse its core logic for:

- HTTP session management (headers, cookies, proxies, retries)
- Parsing video information from URLs
- Multi-threaded downloading with progress bars

You usually do **not** instantiate `BaseVideoClient` directly. Instead, you work with a subclass defined in `VideoClientBuilder.REGISTERED_MODULES` and `CommonVideoClientBuilder.REGISTERED_MODULES`, for example:

- `videodl.modules.sources.AcFunVideoClient`
- `videodl.modules.sources.BilibiliVideoClient`
- `videodl.modules.sources.XiguaVideoClient`
- `videodl.modules.sources.YouTubeVideoClient`
- `videodl.modules.sources.CCTVVideoClient`
- `videodl.modules.sources.YoukuVideoClient`
- `videodl.modules.sources.KuaishouVideoClient`
- `videodl.modules.sources.WeiboVideoClient`
- `videodl.modules.sources.KakaoVideoClient`
- `videodl.modules.sources.OasisVideoClient`
- `videodl.modules.sources.TedVideoClient`
- `videodl.modules.sources.HaokanVideoClient`
- `videodl.modules.sources.BaiduTiebaVideoClient`
- `videodl.modules.sources.MeipaiVideoClient`
- `videodl.modules.sources.SixRoomVideoClient`
- `videodl.modules.sources.RednoteVideoClient`
- `videodl.modules.sources.MGTVVideoClient`
- `videodl.modules.sources.HuyaVideoClient`
- ...
- `videodl.modules.common.BugPkVideoClient`
- `videodl.modules.common.SnapAnyVideoClient`
- `videodl.modules.common.XMFlvVideoClient`
- `videodl.modules.common.KedouVideoClient`
- `videodl.modules.common.QZXDPToolsVideoClient`
- ...

These subclasses share the same initialization pattern and public APIs (`parsefromurl`, `download`) defined by `BaseVideoClient`.

`BaseVideoClient()` accept the following arguments,

- **auto_set_proxies**: `bool`, default `False`  
  Whether to automatically obtain and set HTTP proxies via `freeproxy.ProxiedSessionClient` (refer to [freeproxy](https://github.com/CharlesPikachu/freeproxy/)) for each request.  
  - If `True`, `self.proxied_session_client` is initialized with `proxy_sources`.  
  - If `False`, no automatic proxy management is used (proxies are cleared in `get`/`post`).

- **random_update_ua**: `bool`, default `False`  
  Whether to randomly update the `User-Agent` header every time a new session is created.  
  - If `True`, `UserAgent().random` is used before each request (when `maintain_session=False`).

- **max_retries**: `int`, default `5`  
  Maximum number of retry attempts for `get` and `post` requests.  
  - On each attempt:
    - Session may be reinitialized (depending on `maintain_session`).
    - A proxy may be set (if `auto_set_proxies=True`).
  - If all attempts fail or never return status code `200`, the last `resp` (or `None`) is returned.

- **maintain_session**: `bool`, default `False`  
  Controls whether to reuse the same `requests.Session` across multiple requests.  
  - If `False`, `_initsession()` is called inside each `get`/`post` loop, resetting the session.  
  - If `True`, the same session is reused, preserving cookies and other state.

- **logger_handle**: `LoggerHandle | None`, default `None`  
  Logger used for info and error messages.  
  - If `None`, a new `LoggerHandle()` instance is created.

- **disable_print**: `bool`, default `False`  
  Whether to suppress printing to stdout.  
  - Passed to `logger_handle` to control console output.  
  - Also used to decide whether external commands like `ffmpeg` capture their output or print directly.

- **work_dir**: `str`, default `'videodl_outputs'`  
  Root directory for saving downloaded videos and temporary files.  
  - Created automatically via `touchdir(work_dir)` if it does not exist.  
  - Subclasses often use `os.path.join(self.work_dir, self.source, ...)` to organize per-site outputs.

- **proxy_sources**: `list[str] | None`, default `None`  
  List of proxy provider class names for `freeproxy.ProxiedSessionClient`.  
  - If `None` and `auto_set_proxies=True`, a default list is used internally:  
    `['KuaidailiProxiedSession', 'IP3366ProxiedSession', 'QiyunipProxiedSession', 'ProxyhubProxiedSession', 'ProxydbProxiedSession']`.

- **default_search_cookies**: `dict | None`, default `None`  
  Default cookies for **search-type** requests.  
  - Used by methods decorated with `@usesearchheaderscookies`.

- **default_download_cookies**: `dict | None`, default `None`  
  Default cookies for **download** requests.  
  - Used by methods decorated with `@usedownloadheaderscookies`.

- **default_parse_cookies**: `dict | None`, default `None`  
  Default cookies for **parse** requests.
  - Used by methods decorated with `@useparseheaderscookies`.

Basic initialization example (for a subclass):

```python
from videodl.modules.source import BilibiliVideoClient

client = BilibiliVideoClient(
    work_dir="videodl_outputs", auto_set_proxies=True, random_update_ua=True, max_retries=5, maintain_session=False,
)
```

#### `BaseVideoClient.parsefromurl`

**Abstract method.** Subclasses must implement this to parse video metadata and download information from a given URL.

Arguments:

- **url**: `str`  
  Video page URL belonging to the specific site handled by the subclass.  
  Typically, `BaseVideoClient.belongto(url, valid_domains=[...])` can be used elsewhere to check ownership.

- **request_overrides**: `dict | None`, default `None`  
  Optional per-call overrides for HTTP requests, usually including:
  - `headers`: custom HTTP headers.  
  - `cookies`: custom cookies (e.g., login/session cookies).  
  - `proxies`: if a special proxy configuration is required.

Return Values:

A `list` of video information entries. Each entry should conform to the `VideoInfo` structure used in the library. At minimum, each entry must include:

- `download_url`:  
  - Direct media URL (e.g. `.mp4`, `.m3u8`), or  
  - Path to a local playlist text file for ffmpeg-based workflows.
- `file_path`: target path for saving the downloaded file.
- `source`: identifier for the client, usually the class-level `source` attribute  
  (e.g. `'YouTubeVideoClient'`, `'BilibiliVideoClient'`).

#### `BaseVideoClient.download`

Download one or more videos based on the parsed `video_infos` list.

Arguments:

- **video_infos**: `list[VideoInfo | dict]`  
  List of video info entries, typically returned by `parsefromurl`.  
  Each entry must contain a non-empty `download_url` that is not `'NULL'`.  
  Entries that do not meet this condition are filtered out.

- **num_threadings**: `int`, default `5`  
  Maximum number of concurrent download threads.  
  Each thread calls the internal `_download` method for one `video_info`.

- **request_overrides**: `dict | None`, default `None`  
  Per-call overrides for download requests:
  - `headers`, `cookies`, `proxies` etc.  
  These are merged with `default_download_headers` and `default_download_cookies` via `@usedownloadheaderscookies` and passed to `_download`.

Return Values:

- `list` of successfully downloaded video entries.  
  Each entry corresponds to one of the input `video_infos` and contains the final `file_path` on disk.


