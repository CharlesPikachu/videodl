'''
Function:
    Implementation of PipixVideoClient
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
from ..utils import legalizestring, useparseheaderscookies, resp2json, FileTypeSniffer


'''PipixVideoClient'''
class PipixVideoClient(BaseVideoClient):
    source = 'PipixVideoClient'
    def __init__(self, **kwargs):
        super(PipixVideoClient, self).__init__(**kwargs)
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
            item_id = re.findall(r'item/(\d+)', url)[0]
            resp = self.get(f"https://api.pipix.com/bds/cell/cell_comment/?offset=0&cell_type=1&api_version=1&cell_id={item_id}&ac=wifi&channel=huawei_1319_64&aid=1319&app_name=super", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            data = raw_data["data"]["cell_comments"][0]["comment_info"]["item"]
            author_id, download_url = data["author"]["id"], ""
            for comment in data.get("comments", []):
                if comment["item"]["author"]["id"] == author_id  and comment["item"]["video"]["video_high"]["url_list"][0]["url"]:
                    download_url = comment["item"]["video"]["video_high"]["url_list"][0]["url"]
            if not download_url: download_url = data["video"]["video_high"]["url_list"][0]["url"]
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                data.get('content', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
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
            valid_domains = ['h5.pipix.com']
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)