'''
Function:
    Implementation of YinyuetaiVideoClient
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
from urllib.parse import urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, FileTypeSniffer


'''YinyuetaiVideoClient'''
class YinyuetaiVideoClient(BaseVideoClient):
    source = 'YinyuetaiVideoClient'
    def __init__(self, **kwargs):
        super(YinyuetaiVideoClient, self).__init__(**kwargs)
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
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            resp = self.get(f'https://video-api.yinyuetai.com/video/get?id={vid}', **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            candidate_urls = raw_data["data"]["fullClip"]["urls"]
            candidate_urls = [u for u in candidate_urls if u.get('url')]
            def _sortkey(s: dict):
                disp = s.get("display", "")
                is_mp3 = "MP3" in disp or s.get("streamType") == 5
                bitrate = int(m.group(1)) if (m := re.search(r"(\d+)", disp)) else 0
                return (is_mp3, -bitrate)
            candidate_urls = sorted(candidate_urls, key=_sortkey)
            download_url = candidate_urls[0]['url']
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data["data"].get('title', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, request_overrides=request_overrides)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if ext in ['m3u8']:
                ext = 'mp4'
                video_info.update(dict(download_with_ffmpeg=True, ext=ext))
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
            valid_domains = ["www.yinyuetai.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)