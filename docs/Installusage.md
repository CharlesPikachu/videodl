# 安装使用


#### 环境配置

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+
- ffmpeg: 部分视频为m3u8格式, 需要借助[ffmpeg](https://ffmpeg.org/)解码, 因此需要保证电脑中存在ffmpeg并在环境变量中。
- Nodejs: 部分视频网站(例如西瓜视频)里的信息需要依赖js来进行解码, 因此你需要在电脑上安装[nodejs](https://nodejs.org/en/)来正常下载这些网站上的视频。


#### PIP安装

在终端运行如下命令即可(请保证python在环境变量中):

```sh
pip install videofetch --upgrade
```


#### 源代码安装

**1.在线安装**

运行如下命令即可在线安装:

```sh
pip install git+https://github.com/CharlesPikachu/videodl.git@master
```

**2.离线安装**

利用如下命令下载videodl源代码到本地:

```sh
git clone https://github.com/CharlesPikachu/videodl.git
```

接着, 切到videodl目录下:

```sh
cd videodl
```

最后运行如下命令进行安装:

```sh
python setup.py install
```


#### 快速开始

**1.通过利用编译文件运行**

在终端运行如下命令：

```sh
Usage: videodl [OPTIONS]

Options:
  -i, --url TEXT          想要下载的视频链接, 若不指定, 则进入videodl终端版
  -l, --logfilepath TEXT  日志文件保存的路径
  -p, --proxies TEXT      设置的代理
  -s, --savedir TEXT      视频保存的文件夹
  --help                  Show this message and exit.
```

然后根据相应的提示进行操作即可，效果如下：

<div align="center">
  <img src="https://github.com/CharlesPikachu/videodl/raw/master/docs/screenshot.gif" width="600"/>
</div>
<br />

**2.通过利用API运行**

安装完成后，简单写一段脚本：

```python
from videodl import videodl

config = {
    "logfilepath": "videodl.log",
    "proxies": {},
    "savedir": "downloaded"
}
dl_client = videodl.videodl(config=config)
dl_client.run()
```

即可运行我们的视频下载器。config中各参数含义如下:

- logfilepath: 日志文件保存路径；
- proxies: 设置代理, 支持的代理格式参见[Requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies)；
- savedir: 下载的视频保存路径。

然后根据相应的提示进行操作即可，效果如下：

<div align="center">
  <img src="https://github.com/CharlesPikachu/videodl/raw/master/docs/screenshot.gif" width="600"/>
</div>
<br />