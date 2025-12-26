'''
Function:
    Implementation of M1905VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import math
import random
import hashlib
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse, quote
from ..utils import legalizestring, useparseheaderscookies, FileTypeSniffer, VideoInfo


'''M1905VideoClient'''
class M1905VideoClient(BaseVideoClient):
    source = 'M1905VideoClient'
    def __init__(self, **kwargs):
        super(M1905VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "content-type": "application/json",
            "host": "profile.m1905.com",
            "origin": "https://www.1905.com",
            "referer": "https://www.1905.com/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnQiOiJmZDYwNWM1NjU3ZTJmOWY3IiwiZXhwIjoxNzY2Njc1MzgyLCJub25jZSI6IjNjYjU5MmYwMzYxNGJkNzRmMzhiNGVhNDRiYzVlZTRmIiwidCI6MTc2NjY3NTA4MiwidmlkZW9pZCI6IjE3NTE1MzgifQ.s9BMwTIMCjQtw2tg7_lZJzt5tdAl3WHPsNvdEgknAgM",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_randomplayerid'''
    def _randomplayerid(self):
        def _translate(c):
            n = math.floor(16 * random.random())
            t = "{:x}".format(n) if 'x' == c else "{:x}".format(3 & n | 8) if 'y' == c else c
            return t
        random.seed()
        return ''.join(map(_translate, "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")).replace('-', '')[5: 20]
    '''_signature'''
    def _signature(self, params: dict, appid: str = "dde3d61a0411511d"):
        query, ks = "", sorted(params.keys())
        for k in ks:
            if k != "signature":
                q = k + "=" + quote(str(params[k]), safe="")
                query += "&" + q if query else q
        return hashlib.sha1((query + "." + appid).encode("utf-8")).hexdigest()
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
            vid = parsed_url.path.strip('/').split('.')[0]
            resp = self.post("https://profile.m1905.com/mvod/generate_token.php", **request_overrides)

            resp = self.post(f"https://profile.m1905.com/mvod/playback_assets.php", json={"videoid": vid, "type": "mp4"}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp.json()
            video_info.update(dict(raw_data=raw_data))
            print(video_info)
            return
            for rate in sorted(raw_data["data"]["apiData"]["curVideoMeta"]['clarityUrl'], key=lambda x: float(x['videoSize']), reverse=True):
                download_url = rate.get('url', '')
                if download_url: break
            if not download_url: download_url = raw_data["data"]["apiData"]["curVideoMeta"]['playurl']
            video_info.update(dict(download_url=download_url))
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data["data"]["apiData"]["curVideoMeta"].get('title', f'{self.source}_null_{date_str}'),
                replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=vid,
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
            valid_domains = ["www.1905.com", "vip.1905.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)