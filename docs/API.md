# Videodl APIs


## `videodl.videodl.VideoClient`

#### `VideoClient`

The `VideoClient` class is a high-level manager for multiple site-specific video download clients. It:

- Initializes one internal client per video source.
- Parses video information from a given URL.
- Dispatches download jobs with configurable threading and request overrides.
- Optionally provides an interactive command-line UI.

`VideoClient()` accept the following arguments,

- **allowed_video_sources**: `list[str] | None`  
  List of video source names to enable (*e.g.* `["YouTubeVideoClient"`, `"ZhihuVideoClient"]`).  
  - If `None` or empty, it defaults to **all** sources registered in `VideoClientBuilder.REGISTERED_MODULES`.
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
