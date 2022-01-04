'''
Function:
    视频下载器基类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import requests
from ..utils import Downloader


'''视频下载器基类'''
class Base():
    def __init__(self, config, logger_handle, **kwargs):
        self.source = None
        self.session = requests.Session()
        self.session.proxies.update(config['proxies'])
        self.config = config
        self.logger_handle = logger_handle
    '''视频解析'''
    def parse(self, url):
        raise NotImplementedError('not be implemented...')
    '''歌曲下载'''
    def download(self, videoinfos):
        for videoinfo in videoinfos:
            self.logger_handle.info('正在从%s下载 ——> %s...' % (self.source, videoinfo['savename']))
            task = Downloader(videoinfo.copy(), self.session)
            if task.start():
                self.logger_handle.info('成功从%s下载到了 ——> %s...' % (self.source, videoinfo['savename']))
            else:
                self.logger_handle.info('无法从%s下载 ——> %s...' % (self.source, videoinfo['savename']))
    '''初始化'''
    def __initialize(self):
        raise NotImplementedError('not be implemented...')
    '''返回类信息'''
    def __repr__(self):
        return 'Video Source: %s' % self.source
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        raise NotImplementedError('not be implemented...')