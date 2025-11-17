'''
Function:
    Implementation of BilibiliVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, FileTypeSniffer


'''BilibiliVideoClient'''
class BilibiliVideoClient(BaseVideoClient):
    source = 'BilibiliVideoClient'
    def __init__(self, **kwargs):
        super(BilibiliVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Referer': 'https://www.bilibili.com/',
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
        video_infos = []
        try:
            parsed_url = urlparse(url)
            if "b23.tv" in parsed_url.netloc:
                resp = self.get(url, allow_redirects=True, **request_overrides)
                parsed_url = urlparse(resp.url)
            vid = parsed_url.path.strip("/").split("/")[1]
            resp = self.get(f"https://api.bilibili.com/x/web-interface/view?bvid={vid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            for page_idx, page in enumerate(raw_data['data']["pages"]):
                cid = page['cid']
                resp = self.get(f"https://api.bilibili.com/x/player/playurl?otype=json&fnver=0&fnval=0&qn=80&bvid={vid}&cid={cid}&platform=html5", **request_overrides)
                resp.raise_for_status()
                page_raw_data = resp2json(resp=resp)
                page_raw_data['web-interface'] = copy.deepcopy(raw_data)
                video_page_info = copy.deepcopy(video_info)
                video_page_info.update(dict(raw_data=page_raw_data))
                download_url = max(page_raw_data['data']['durl'], key=lambda x: x['size'])['url']
                video_page_info.update(dict(download_url=download_url))
                video_title = legalizestring(
                    raw_data["data"].get('title', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
                ).removesuffix('.')
                video_title = f"{video_title}_split{page_idx}" if len(raw_data['data']["pages"]) > 1 else video_title
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, request_overrides=request_overrides)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']
                if ext in ['m3u8']:
                    ext = 'mp4'
                    video_page_info.update(dict(download_with_ffmpeg=True, ext=ext))
                video_page_info.update(dict(
                    video_title=video_title, file_path=os.path.join(self.work_dir, self.source, video_title + f'.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result,
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}.parsefromurl >>> {url} (Error: {err})', disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.bilibili.com", "b23.tv"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)