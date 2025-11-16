'''
Function:
    皮皮搞笑视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import json
from .base import Base
from ..utils import filterBadCharacter


'''皮皮搞笑视频下载器类'''
class Pipigaoxiao(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Pipigaoxiao, self).__init__(config, logger_handle, **kwargs)
        self.source = 'pipigaoxiao'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
        url = re.findall(pattern, url)[0]
        self.headers['Referer'] = url
        try:
            mid = re.findall('mid=(\d+)', url, re.S)[0]
            pid = re.findall('pid=(\d+)', url, re.S)[0]
        except:
            mid = ''
            pid = url.split('/')[-1]
        data = {
            'mid': int(mid) if mid else 'null',
            'pid': int(pid),
            'type': 'post',
        }
        response = self.session.post(self.content_url, data=json.dumps(data), headers=self.headers)
        response_json = response.json()
        download_url = response_json['data']['post']['videos'][str(response_json['data']['post']['imgs'][0]['id'])]['url']
        title = response_json['data']['post']['content'].replace('\n', '')
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(title),
            'ext': 'mp4',
        }
        return [videoinfo]
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'Host': 'share.ippzone.com',
            'Origin': 'http://share.ippzone.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        }
        self.content_url = 'https://h5.ippzone.com/ppapi/share/fetch_content'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['h5.ippzone.com', 'share.ippzone.com']
        for host in valid_hosts:
            if host in url: return True
        return False