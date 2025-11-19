'''
Function:
    Implementation of Ku6VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
from datetime import datetime
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, FileTypeSniffer, VideoInfo


'''Ku6VideoClient'''
class Ku6VideoClient(BaseVideoClient):
    source = 'Ku6VideoClient'
    def __init__(self, **kwargs):
        super(Ku6VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Referer': 'https://www.ku6.com/index',
            'Host': 'www.ku6.com',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        # try parse
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            raw_data = resp.text
            video_info.update(dict(raw_data=raw_data))
            pattern = r'this\.src\(\s*\{.*?src\s*:\s*["\']([^"\']+)["\']'
            download_url = re.search(pattern, raw_data, re.S).group(1) or re.findall(r'src: "(https://.*?)"', raw_data)[0]
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            title = re.findall(r'document.title = "(.*?)";', raw_data) or f'{self.source}_null_{date_str}'
            if isinstance(title, list): title = title[0]
            video_title = legalizestring(title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result,
            ))
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.ku6.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)