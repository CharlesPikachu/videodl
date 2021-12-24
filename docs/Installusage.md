# 安装使用


## PIP安装
在终端运行如下命令即可(请保证python在环境变量中):
```sh
pip install videofetch --upgrade
```


## 源代码安装

#### 在线安装
运行如下命令即可在线安装:
```sh
pip install git+https://github.com/CharlesPikachu/videodl.git@master
```

#### 离线安装
利用如下命令下载videodl源代码到本地:
```sh
git clone https://github.com/CharlesPikachu/videodl.git
```
接着, 切到musicdl目录下:
```sh
cd videodl
```
最后运行如下命令进行安装:
```sh
python setup.py install
```


## 快速开始
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
```
logfilepath: 日志文件保存路径
proxies: 设置代理, 支持的代理格式参见https://requests.readthedocs.io/en/master/user/advanced/#proxies
savedir: 下载的音乐保存路径  
```