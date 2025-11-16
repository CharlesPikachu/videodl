'''
Function:
    搜狐视频下载器类
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
from .base import Base
from ..utils import filterBadCharacter


'''搜狐视频下载器类'''
class Sohu(Base):
    def __init__(self, config, logger_handle, **kwargs):
        super(Sohu, self).__init__(config, logger_handle, **kwargs)
        self.source = 'sohu'
        self.__initialize()
    '''视频解析'''
    def parse(self, url):
        if re.match(r'http://share.vrs.sohu.com', url):
            vid = r1('id=(\d+)', url)
        else:
            response = self.session.get(url, headers=self.headers)
            vid = re.findall(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?', response.text) or re.findall(r'bid:\'(\d+)\',', response.text) or re.findall(r'bid=(\d+)', response.text)
        if not vid: return []
        params = {'vid': vid[0]}
        response = self.session.get(self.flash_url, params=params, headers=self.headers)
        response_json = response.json()
        if response_json and response_json.get('data', ''):
            for qtyp in ['oriVid', 'superVid', 'highVid', 'norVid', 'relativeId']:
                hqvid = response_json['data'][qtyp]
                if hqvid != 0 and hqvid != vid[0]:
                    params = {'vid': hqvid}
                    response = self.session.get(self.flash_url, params=params, headers=self.headers)
                    if 'allot' not in response.json(): continue
                    response_json = response.json()
                    break
        else:
            url = f'http://my.tv.sohu.com/play/videonew.do?vid={vid[0]}&referer=http://my.tv.sohu.com'
            response = self.session.get(url, headers=self.headers)
            response_json = response.json()
        title = response_json['data']['tvName']
        assert len(response_json['data']['clipsURL']) == len(response_json['data']['clipsBytes']) == len(response_json['data']['su'])
        download_url = []
        for su, ck in zip(response_json['data']['su'], response_json['data']['ck']):
            download_url.append(self.converttorealurl(su, ck, response_json['data']['ch']))
        if len(download_url) == 1: download_url = download_url[0]
        videoinfo = {
            'source': self.source,
            'download_url': download_url,
            'savedir': self.config['savedir'],
            'savename': filterBadCharacter(title or f'视频走丢啦_{time.time()}'),
            'ext': 'mp4',
            'split_ext': 'mp4',
        }
        return [videoinfo]
    '''获得真实下载链接'''
    def converttorealurl(self, su, ck, ch):
        url = f'https://data.vod.itc.cn/ip?new={su}&num=1&key={ck}&ch={ch}&pt=1&pg=2&prod=h5n'
        response = self.session.get(url, headers=self.headers)
        return response.json()['servers'][0]['url']
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        }
        self.flash_url = 'https://hot.vrs.sohu.com/vrs_flash.action'
    '''判断视频链接是否属于该类'''
    @staticmethod
    def isurlvalid(url):
        valid_hosts = ['sohu.com']
        for host in valid_hosts:
            if host in url: return True
        return False