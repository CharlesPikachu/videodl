'''
Function:
    Implementation of TedVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json_repair
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''TedVideoClient'''
class TedVideoClient(BaseVideoClient):
    source = 'TedVideoClient'
    def __init__(self, **kwargs):
        super(TedVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            "accept-encoding": "identity;q=1, *;q=0",
            "referer": "https://www.ted.com/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
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
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, "lxml")
            script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
            raw_data = json_repair.loads(script_tag.string)
            video_info.update(dict(raw_data=raw_data))
            player_data = json_repair.loads(raw_data["props"]["pageProps"]["videoData"]["playerData"])
            download_url = safeextractfromdict(player_data, ['resources', 'hls', 'stream'], '') or \
                           safeextractfromdict(sorted(safeextractfromdict(player_data, ['resources', 'h264'], []), key=lambda x: x.get('bitrate', 0), reverse=True), [0, 'file'], '') or \
                           safeextractfromdict(sorted(safeextractfromdict(player_data, ['resources', 'rtmp'], []), key=lambda x: x.get('width', 0) * x.get('height', 0), reverse=True), [0, 'file'], '')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(download_url=download_url))
            video_title = raw_data["props"]["pageProps"]["videoData"].get('title', null_backup_title) or null_backup_title
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid,
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
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"ted.com"}
        return BaseVideoClient.belongto(url, valid_domains)