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
from urllib.parse import urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, FileTypeSniffer, VideoInfo


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
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        # try parse
        video_infos = []
        try:
            # --redirect
            parsed_url = urlparse(url)
            if "b23.tv" in parsed_url.netloc:
                resp = self.get(url, allow_redirects=True, **request_overrides)
                parsed_url = urlparse(resp.url)
            # --basic info from vid
            vid = parsed_url.path.strip("/").split("/")[1]
            resp = self.get(f"https://api.bilibili.com/x/web-interface/view?bvid={vid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            # --iter to parse
            for _, page in enumerate(raw_data['data']["pages"]):
                cid = page['cid']
                resp = self.get(f"https://api.bilibili.com/x/player/playurl?otype=json&fnver=0&fnval=0&qn=80&bvid={vid}&cid={cid}&platform=html5", **request_overrides)
                resp.raise_for_status()
                page_raw_data = resp2json(resp=resp)
                page_raw_data['web-interface'] = copy.deepcopy(raw_data)
                video_page_info = copy.deepcopy(video_info)
                video_page_info.update(dict(raw_data=page_raw_data))
                durl = page_raw_data['data']['durl']
                durl = [x for x in durl if x.get('url')]
                download_url = max(page_raw_data['data']['durl'], key=lambda x: x['size'])['url']
                video_page_info.update(dict(download_url=download_url))
                video_title = legalizestring(
                    raw_data["data"].get('title', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
                ).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_page_info['ext']
                video_page_info.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result,
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.bilibili.com", "b23.tv"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)