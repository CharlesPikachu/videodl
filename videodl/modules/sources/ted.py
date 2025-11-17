'''
Function:
    Implementation of TedVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import json_repair
from bs4 import BeautifulSoup
from datetime import datetime
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, FileTypeSniffer


'''TedVideoClient'''
class TedVideoClient(BaseVideoClient):
    source = 'TedVideoClient'
    def __init__(self, **kwargs):
        super(TedVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = {}):
        # prepare
        video_info = {
            'source': self.source, 'raw_data': 'NULL', 'download_url': 'NULL', 'video_title': 'NULL', 'file_path': 'NULL', 
            'ext': 'mp4', 'download_with_ffmpeg': False,
        }
        if not self.belongto(url=url): return [video_info]
        # try parse
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, "lxml")
            script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
            raw_data = json_repair.loads(script_tag.string)
            video_info.update(dict(raw_data=raw_data))
            player_data = json_repair.loads(raw_data["props"]["pageProps"]["videoData"]["playerData"])
            try:
                download_url = player_data["resources"]['h264'][0]['file']
            except:
                download_url = player_data["resources"]['stream']
                video_info.update(dict(download_with_ffmpeg=True))
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = raw_data["props"]["pageProps"]["videoData"]["title"]
            video_title = video_title if video_title else f'{self.source}_null_{date_str}'
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, request_overrides=request_overrides)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                video_title=video_title, file_path=os.path.join(self.work_dir, self.source, video_title + f'.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result,
            ))
        except Exception as err:
            self.logger_handle.error(f'{self.source}.parsefromurl >>> {url} (Error: {err})', disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["ted.com", "www.ted.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)