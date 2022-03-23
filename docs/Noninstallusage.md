# 直接使用


#### 环境配置

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+
- ffmpeg: 部分视频为m3u8格式, 需要借助[ffmpeg](https://ffmpeg.org/)解码, 因此需要保证电脑中存在ffmpeg并在环境变量中。
- Nodejs: 部分视频网站(例如西瓜视频)里的信息需要依赖js来进行解码, 因此你需要在电脑上安装[nodejs](https://nodejs.org/en/)来正常下载这些网站上的视频。


#### 项目下载

运行如下命令下载项目:

```sh
git clone https://github.com/CharlesPikachu/videodl.git
```


#### 配置文件

在videodl文件夹中有config.json文件, 该文件为配置文件, 文件中各参数含义如下:

- logfilepath: 日志文件保存路径；
- proxies: 设置代理, 支持的代理格式参见[Requests](https://requests.readthedocs.io/en/master/user/advanced/#proxies)；
- savedir: 下载的视频保存路径。


#### 项目运行

在终端执行如下命令:

```sh
python videodl.py
```

然后根据相应的提示进行操作即可，效果如下：

<div align="center">
  <img src="https://github.com/CharlesPikachu/videodl/raw/master/docs/screenshot.gif" width="600"/>
</div>
<br />