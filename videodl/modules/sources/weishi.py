'''
Function:
    Implementation of WeishiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, FileTypeSniffer, VideoInfo


'''WeishiVideoClient'''
class WeishiVideoClient(BaseVideoClient):
    source = 'WeishiVideoClient'
    def __init__(self, **kwargs):
        super(WeishiVideoClient, self).__init__(**kwargs)
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
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        # try parse
        try:
            parsed_url = urlparse(url)
            if 'id' in parse_qs(parsed_url.query, keep_blank_values=True):
                vid = parse_qs(parsed_url.query, keep_blank_values=True)['id'][0]
            else:
                vid = parsed_url.path.strip('/').split('/')[-1]
            resp = self.get(f"https://h5.weishi.qq.com/webapp/json/weishi/WSH5GetPlayPage?feedid={vid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            specs = raw_data["data"]["feeds"][0]["video_spec_urls"]
            sorted_specs = sorted(specs.items(), key=lambda kv: kv[1].get("size", 0), reverse=True)
            for _, ss in sorted_specs:
                download_url = ss.get('url', "")
                if download_url: break
            if not download_url: download_url = raw_data["data"]["feeds"][0]["video_url"]
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data["data"]["feeds"][0].get('feed_desc_withat', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
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
            valid_domains = ["isee.weishi.qq.com", "h5.weishi.qq.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)