'''
Function:
    视频下载器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import copy
import json
import click
import warnings
if __name__ == '__main__':
    from modules import *
    from __init__ import __version__
else:
    from .modules import *
    from .__init__ import __version__
warnings.filterwarnings('ignore')


'''basic info'''
BASICINFO = '''************************************************************
Function: 视频下载器 V%s
Author: Charles
微信公众号: Charles的皮卡丘
操作帮助:
    输入r: 重新初始化程序(即返回主菜单)
    输入q: 退出程序
视频保存路径:
    当前路径下的%s文件夹内
************************************************************'''


'''视频下载器'''
class videodl():
    def __init__(self, configpath=None, config=None, **kwargs):
        assert configpath or config, 'configpath of config should be given'
        self.config = loadConfig(configpath) if config is None else config
        self.logger_handle = Logger(self.config['logfilepath'])
        self.supported_sources = self.initializeAllSources()
    '''非开发人员外部调用'''
    def run(self):
        print(BASICINFO % (__version__, self.config.get('savedir')))
        while True:
            # 视频链接输入
            user_input = self.dealInput('请输入视频链接: ')
            # 判断视频链接类型是否支持解析下载
            source = self.findsource(user_input)
            if source is None:
                self.logger_handle.warning('暂不支持解析视频链接: %s' % user_input)
                continue
            # 实例化
            client = source(self.config, self.logger_handle)
            # 视频链接解析
            videoinfos = client.parse(user_input)
            # 视频下载
            client.download(videoinfos)
    '''判断视频源'''
    def findsource(self, url):
        for key, source in self.supported_sources.items():
            if source.isurlvalid(url): return source
        return None
    '''初始化所有支持的搜索/下载源'''
    def initializeAllSources(self):
        supported_sources = {
            'ted': Ted, 'cntv': CNTV, 'mgtv': MGTV, 'migu': Migu,
            'pipix': Pipix, 'acfun': AcFun, 'zhihu': Zhihu, 'xigua': Xigua,
            'iqiyi': Iqiyi, 'douyin': Douyin, 'haokan': Haokan, 'bilibili': Bilibili, 
            'yinyuetai': Yinyuetai, 'pipigaoxiao': Pipigaoxiao, 'weibo': Weibo, 'ku6': Ku6,
            'baidutieba': BaiduTieba, 'kuaishou': Kuaishou, 'sohu': Sohu,
        }
        return supported_sources
    '''处理用户输入'''
    def dealInput(self, tip=''):
        user_input = input(tip)
        if user_input.lower() == 'q':
            self.logger_handle.info('ByeBye')
            sys.exit()
        elif user_input.lower() == 'r':
            self.supported_sources = self.initializeAllSources()
            self.run()
        else:
            return user_input
    '''str'''
    def __str__(self):
        return 'Welcome to use videodl!\nYou can visit https://github.com/CharlesPikachu/videodl for more details.'


'''cmd直接运行'''
@click.command()
@click.option('-i', '--url', default=None, help='想要下载的视频链接, 若不指定, 则进入videodl终端版')
@click.option('-l', '--logfilepath', default='videodl.log', help='日志文件保存的路径')
@click.option('-p', '--proxies', default='{}', help='设置的代理')
@click.option('-s', '--savedir', default='videos', help='视频保存的文件夹')
def videodlcmd(url, logfilepath, proxies, savedir):
    config = {
        'logfilepath': logfilepath,
        'proxies': json.loads(proxies),
        'savedir': savedir,
    }
    dl_client = videodl(config=config)
    if url is None:
        dl_client.run()
    else:
        print(dl_client)
        source = dl_client.findsource(url)
        client = source(dl_client.config, dl_client.logger_handle)
        videoinfos = client.parse(url)
        client.download(videoinfos)


'''run'''
if __name__ == '__main__':
    import os
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    dl_client = videodl(os.path.join(rootdir, 'config.json'))
    dl_client.run()