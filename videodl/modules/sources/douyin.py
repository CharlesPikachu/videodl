'''
Function:
    抖音视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import json
import time
import random
import requests
from .base import Base
from ..utils.misc import *


'''抖音视频下载器类'''
class Douyin(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Douyin, self).__init__(config, logger_handle, **kwargs)
        self.source = 'douyin'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)[0]
        response = self.session.get(url)
        if response.url[:28] == 'https://www.douyin.com/user/':
            videoinfos = self.multiparse(response)
        else:
            videoinfos = self.singleparse(response)
        return videoinfos
    '''批量下载用户的视频'''
    def multiparse(self, response):
        videoinfos = []
        key = re.findall(r'/user/(.*?)\?', str(response.url))[0]
        if not key: key = response.url[28: 83]
        page_count, max_cursor = 35, 0
        while True:
            url = self.uid_url.format('post', key, page_count, max_cursor)
            response = self.session.get(url, headers=self.headers)
            response_json = json.loads(response.content.decode())
            max_cursor, aweme_list = response_json['max_cursor'], response_json['aweme_list']
            if max_cursor == 0: break
            for idx in range(min(page_count, len(aweme_list))):
                download_url = str(aweme_list[idx].get('video', {}).get('play_addr', {}).get('url_list', [''])[0])
                videoinfo = {
                    'source': self.source,
                    'aweme_id': aweme_list[idx].get('aweme_id', None),
                    'download_url': download_url,
                    'savedir': self.config['savedir'],
                    'savename': '_'.join([self.source, filterBadCharacter(str(aweme_list[idx].get('desc', f'视频走丢啦_{time.time()}')))]),
                    'ext': 'mp4',
                }
                if videoinfo['download_url']: videoinfos.append(videoinfo)
            time.sleep(random.random() + 0.2)
        return videoinfos
    '''下载单个视频'''
    def singleparse(self, response):
        url = self.iteminfo_url.format(re.findall(r'video/(\d+)?', str(response.url))[0])
        response_json = json.loads(self.session.get(url, headers=self.headers).text)
        try: download_url = str(response_json['item_list'][0]['video']['play_addr']['url_list'][0]).replace('playwm','play')
        except: return []
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': '_'.join([self.source, filterBadCharacter(str(response_json.get('item_list', [{}])[0].get('desc', f'视频走丢啦_{time.time()}')))]),
            'ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66',
        }
        self.iteminfo_url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={}'
        self.uid_url = 'https://www.iesdouyin.com/web/api/v2/aweme/{}/?sec_uid={}&count={}&max_cursor={}&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk='
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['v.douyin.com']
        for host in valid_hosts:
            if host in url: return True
        return False