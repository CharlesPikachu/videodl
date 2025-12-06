# Videodl Installation

#### Environment Requirements

- Operating system: Linux, macOS, or Windows.
- Python version: Python 3.9+ with requirements in [videodl requirements.txt](https://github.com/CharlesPikachu/videodl/blob/master/requirements.txt).

#### Installation Instructions

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

Some of the video downloaders supported by `videodl` rely on additional CLI tools to enable video decryption, stream parsing and downloading, accelerated stream downloading, and other extended features such as resuming interrupted downloads. 
Specifically, these CLI tools include,

- **[FFmpeg](https://ffmpeg.org/)**: All video downloaders that need to handle HLS (HTTP Live Streaming) streams depend on FFmpeg. Therefore, we recommend that all `videodl` users install FFmpeg.
  Specifically, you need to ensure that, after installation, FFmpeg can be invoked directly from your system environment (*i.e.*, it is on your `PATH`).
  A quick way to verify this is to open a terminal (or Command Prompt on Windows) and run,
  ```bash
  ffmpeg -version
  ```
  If the installation is correct, you should see detailed version information instead of a "command not found" or "'ffmpeg' is not recognized" error.
  
- **[CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) and [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI)**: 
  These two CLI tools are only used to fix the issue of corrupted (garbled) video when downloading HD videos with `CCTVVideoClient` due to encrypted m3u8 links. 
  You only need to download [CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) from the GitHub releases and add the path to cbox to your environment variables.
  If you don’t need to use `CCTVVideoClient` to download HD videos, you don’t need to configure these two CLI tools.
  As with FFmpeg, after installation you should make sure these tools can be run directly from the command line, *i.e.*, their location is included in your system `PATH`.
  A quick way to verify this is that you should be able to run
  ```bash
  python -c "import shutil; print(shutil.which('cbox'))"
  python -c "import shutil; print(shutil.which('N_m3u8DL-CLI'))"
  ```
  in Command Prompt and get the full path without an error.
  If the N_m3u8DL-CLI version is not compatible with your system, please download the appropriate one from the [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI) official website yourself.

- **[Node.js](https://nodejs.org/en)**: Currently, Node.js is only used in `YouTubeVideoClient` to execute certain JavaScript code for video parsing. 
  Therefore, if you don’t need to use `YouTubeVideoClient`, you can safely skip installing this CLI tool.
  A quick way to check whether Node.js has been installed successfully is to open a terminal (or Command Prompt on Windows) and run:
  ```bash
  node -v (npm -v)
  ```
  If Node.js is installed correctly, `node -v` will print the Node.js version (*e.g.*, `v22.11.0`), and `npm -v` will print the npm version.
  If you see a similar `command not found` / `not recognized` error, Node.js is not installed correctly or not available on your `PATH`.

- **[N_m3u8DL-RE](https://github.com/nilaoda/N_m3u8DL-RE)**: 
  FFmpeg is a general-purpose media tool that can download standard HLS/m3u8 streams, but it assumes that the playlist and segment URLs strictly follow the protocol. 
  N_m3u8DL-RE is a specialized m3u8 downloader that adds extensive logic for handling encryption, anti-leech headers, redirects, and malformed playlists, so it can capture many ‘protected’ or non-standard videos that FFmpeg fails on. 
  Therefore, for some sites where downloading m3u8 streams with FFmpeg is throttled or fails, we recommend installing and using N_m3u8DL-RE instead.
  Currently, the video downloaders that use N_m3u8DL-RE by default include `FoxNewsVideoClient`, `TencentVideoClient`, `GVVIPVideoClient`, `SnapAnyVideoClient`, `VgetVideoClient`, `ArteTVVideoClient` and `IIILabVideoClient`. 
  Therefore, if you don’t need to download videos from these two platforms, you can choose not to install this CLI tool.
  As with FFmpeg, after installation you should make sure this tool can be run directly from the command line, *i.e.*, its location is included in your system `PATH`.
  A quick way to check whether N_m3u8DL-RE has been installed successfully is to open a terminal (or Command Prompt on Windows) and run:
  ```bash
  N_m3u8DL-RE --version
  ```
  If N_m3u8DL-RE is installed correctly, `N_m3u8DL-RE --version` will print the N_m3u8DL-RE version (*e.g.*, `0.5.1+c1f6db5639397dde362c31b31eebd88c796c90da`).
  If you see a similar `command not found` / `not recognized` error, N_m3u8DL-RE is not installed correctly or not available on your `PATH`.

- **[aria2c](https://aria2.github.io/)**: `videodl` now also supports manually integrating aria2c to accelerate downloads (for example, MP4 files) and to enable resuming interrupted video downloads, *etc*. 
  Before using this feature, you must ensure that aria2c is available on the system `PATH` in your runtime environment. 
  You can verify this by opening a terminal and running `aria2c --version` (or `aria2c -v`); if the command returns version information instead of a `“command not found”` error, 
  then aria2c is correctly installed and detectable. On Linux/macOS you can also run `which aria2c`, and on Windows `where aria2c`, to confirm that the executable can be found.
  To enable aria2c during video downloading, please refer to the [Quick Start](https://videofetch.readthedocs.io/zh/latest/Quickstart.html) section.