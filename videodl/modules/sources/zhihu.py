'''
Function:
    知乎视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import json
import time
from .base import Base
from ..utils.misc import *


'''知乎视频下载器类'''
class Zhihu(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Zhihu, self).__init__(config, logger_handle, **kwargs)
        self.source = 'zhihu'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        response = self.session.get(url, headers=self.headers)
        title = re.findall(r'data-react-helmet="true">(.*?)</title>', response.text)
        if title: title = title[0]
        else: title = f'视频走丢啦_{time.time()}'
        videoinfos = []
        for idx, video_id in enumerate(re.findall(r'<a class="video-box" href="\S+video/(\d+)"', response.text)):
            info = json.loads(self.session.get(self.videoapi_url.format(video_id), headers=self.headers).text)
            play_list = info['playlist']
            info = play_list.get('hd', play_list.get('sd', play_list.get('ld', None)))
            if info is None: continue
            download_url = info['play_url']
            videoinfo = {
                'source': self.source,
                'download_url': download_url,
                'savedir': self.config['savedir'],
                'savename': '_'.join([self.source, filterBadCharacter(title + '_' + video_id)]),
                'ext': 'mp4',
            }
            videoinfos.append(videoinfo)
        return videoinfos
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        self.videoapi_url = 'https://lens.zhihu.com/api/videos/{}'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['zhihu.com']
        for host in valid_hosts:
            if host in url: return True
        return False