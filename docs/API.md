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

- **`allowed_video_sources`**:
  
  A list of enabled client names.
  - If this is `None` or empty, `VideoClient` enables all registered clients.
  - Each item should be a client name such as `"AcFunVideoClient"`.
  
  Example:
  ```python
  allowed_video_sources = ["AcFunVideoClient"]
  ```

- **`init_video_clients_cfg`**:

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

- **`clients_threadings`**:

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

- **`requests_overrides`**:
  
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

- **`apply_common_video_clients_only`**:
  
  Whether to use only the generic parsers.
  - `False`: try platform-specific clients first, then generic parsers if needed.
  - `True`: skip platform-specific clients and use only common parsers.
  
  This can be useful when the target URL is not from a built-in supported site.

#### `VideoClient.parsefromurl()`

Parse a video URL and return one or more `VideoInfo` objects.

```python
parsefromurl(url: str) -> list[VideoInfo]
```

Parsing behavior:

When `parsefromurl()` is called, `VideoClient` uses the following strategy:

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


