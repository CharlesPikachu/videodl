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

Also, some video downloaders depend on [Ffmpeg](https://ffmpeg.org/), 
[CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) and 
[N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI), 
so please make sure both programs are installed and can be invoked directly from your system environment (*i.e.*, they are on your PATH). 
A quick way to verify this is:

- **For Ffmpeg**: open a terminal (or Command Prompt on Windows) and run,
  ```bash
  ffmpeg -version
  ```
  If the installation is correct, you should see detailed version information instead of a "command not found" or "'ffmpeg' is not recognized" error.

- **For CBox and N_m3u8DL-CLI (Windows only for CCTVVideoClient)**:
  You only need to download [CBox](https://github.com/CharlesPikachu/videodl/releases/download/software_dependency/cbox.zip) from the GitHub releases and add the path to cbox to your environment variables.
  If you don’t need to download the highest-quality videos from CCTV, you don’t need to install this library.
  If your downloader calls it from the command line, you should also be able to run
  ```bash
  python -c "import shutil; print(shutil.which('cbox'))"
  python -c "import shutil; print(shutil.which('N_m3u8DL-CLI'))"
  ```
  in Command Prompt and get the full path without an error.
  If the N_m3u8DL-CLI version is not compatible with your system, please download the appropriate one from the [N_m3u8DL-CLI](https://github.com/nilaoda/N_m3u8DL-CLI) official website yourself.