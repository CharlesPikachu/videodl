'''
Function:
    Implementation of WeiboVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import json
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, resp2json, useparseheaderscookies, FileTypeSniffer, VideoInfo


'''WeiboVideoClient'''
class WeiboVideoClient(BaseVideoClient):
    source = 'WeiboVideoClient'
    def __init__(self, **kwargs):
        super(WeiboVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'https://weibo.com/',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsehtml'''
    @useparseheaderscookies
    def _parsehtml(self, vid: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            "Referer": f"https://m.weibo.cn/detail/{vid}",
            "X-Requested-With": "XMLHttpRequest",
        }
        # try parse
        try:
            resp = self.get(f"https://m.weibo.cn/statuses/show?id={vid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp)
            video_info.update(dict(raw_data=raw_data))
            download_urls: dict = raw_data['data']['page_info']['urls']
            def _getresolutionscore(url: str):
                m = re.search(r'template=(\d+)x(\d+)', url)
                if not m: return 0
                w, h = int(m.group(1)), int(m.group(2))
                return w * h
            sorted_download_urls = sorted(download_urls.items(), key=lambda kv: _getresolutionscore(kv[1]), reverse=True)
            download_url = sorted_download_urls[0][1] if sorted_download_urls else raw_data['data']['page_info']['media_info']['stream_url']
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data["data"]['page_info'].get('title') or raw_data["data"]['page_info'].get('page_title') or f'{self.source}_null_{date_str}',
                replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result,
            ))
        except Exception as err:
            err_msg = f'{self.source}._parsehtml >>> {vid} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
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
            try:
                vid = parse_qs(parsed_url.query, keep_blank_values=True)['fid'][0]
            except:
                vid = parsed_url.path.strip('/').split('/')[-1]
            if ':' not in vid: return self._parsehtml(vid=vid, request_overrides=request_overrides)
            params = {"page": f"/show/{vid}"}
            payload = {"Component_Play_Playinfo": {"oid": f"{vid}"}}
            self.default_headers['Referer'] = url
            resp = self.post(f'https://h5.video.weibo.com/api/component', params=params, data={"data": json.dumps(payload)}, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            raw_data = resp2json(resp)
            video_info.update(dict(raw_data=raw_data))
            download_urls: dict = raw_data["data"]["Component_Play_Playinfo"]["urls"]
            def _qualityfromkey(k: str):
                m = re.search(r'(\d+)P', k)
                return int(m.group(1)) if m else 0
            sorted_download_urls = sorted(download_urls.items(), key=lambda kv: _qualityfromkey(kv[0]), reverse=True)
            download_url = f"https:{sorted_download_urls[0][1]}" if sorted_download_urls else raw_data["data"]["Component_Play_Playinfo"]["stream_url"]
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data["data"]["Component_Play_Playinfo"].get('title', f'{self.source}_null_{date_str}'),
                replace_null_string=f'{self.source}_null_{date_str}',
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
            valid_domains = ["weibo.com", "m.weibo.cn"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)