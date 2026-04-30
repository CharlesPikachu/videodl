'''
Function:
    Implementation of DailyMotionVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import random
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, safeextractfromdict, VideoInfo, FileTypeSniffer


'''DailyMotionVideoClient'''
class DailyMotionVideoClient(BaseVideoClient):
    source = 'DailyMotionVideoClient'
    ACCESS_TOKEN = None
    CLIENT_ID = 'f1a362d288c1b98099c7'
    CLIENT_SECRET = 'eea605b96e01c796ff369935357eca920c5da4c5'
    generate_blockbuster_headers_func = lambda rnd=(lambda mn, mx: ''.join(random.choices('bcdfghjklmnpqrstvwxz', k=random.randint(mn, mx)))): {rnd(8, 24): rnd(16, 32) for _ in range(random.randint(2, 8))}
    def __init__(self, **kwargs):
        super(DailyMotionVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36", "Referer": "https://www.dailymotion.com/", "Origin": "https://www.dailymotion.com"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36", "Referer": "https://www.dailymotion.com/", "Origin": "https://www.dailymotion.com", **DailyMotionVideoClient.generate_blockbuster_headers_func()}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getaccesstoken'''
    def _getaccesstoken(self, request_overrides: dict = None):
        if DailyMotionVideoClient.ACCESS_TOKEN is not None: return DailyMotionVideoClient.ACCESS_TOKEN
        data = {'client_id': DailyMotionVideoClient.CLIENT_ID, 'client_secret': DailyMotionVideoClient.CLIENT_SECRET, 'grant_type': 'client_credentials'}
        (resp := self.post('https://graphql.api.dailymotion.com/oauth/token', data=data, **(request_overrides or {}))).raise_for_status()
        DailyMotionVideoClient.ACCESS_TOKEN = resp2json(resp=resp)['access_token']
        return DailyMotionVideoClient.ACCESS_TOKEN
    '''_callgraphqlapi'''
    def _callgraphqlapi(self, video_id: str, request_overrides: dict = None):
        self._getaccesstoken(request_overrides=(request_overrides := request_overrides or {}))
        (headers := self.default_headers.copy())['Authorization'] = f'Bearer {DailyMotionVideoClient.ACCESS_TOKEN}'
        query = '{\n          media(xid: "%s") {\n            ... on Video {\n              xid\n              description\n              geoblockedCountries {\n                allowed\n              }\n            }\n            ... on Live {\n              xid\n              description\n              geoblockedCountries {\n                allowed\n              }\n            }\n          }\n        }' % video_id
        (resp := self.post('https://graphql.api.dailymotion.com/', json={'query': query}, headers=headers, **request_overrides)).raise_for_status()
        return resp2json(resp=resp)['data']['media']
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            video_id = re.search(r'(?:video/|dai\.ly/|player\.html\?video=)([a-zA-Z0-9]+)', url).group(1)
            video_info.update(dict(raw_data=(raw_data := self._callgraphqlapi(video_id, request_overrides=request_overrides))))
            (resp := self.get(f"https://www.dailymotion.com/player/metadata/video/{raw_data['xid']}?app=com.dailymotion.neon", **request_overrides)).raise_for_status()
            raw_data['metadata_resp'] = resp2json(resp=resp); qualities: dict = raw_data['metadata_resp']['qualities']
            video_info.update(dict(download_url=str(next((m.get('url') for media_list in qualities.values() for m in media_list if isinstance(m, dict) and m.get('type') == 'application/x-mpegURL'), '')).split('#')[0]))
            video_title = legalizestring(safeextractfromdict(raw_data, ['metadata_resp', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            cover_url = safeextractfromdict(raw_data, ['metadata_resp', 'thumbnails', '1080'], None) or safeextractfromdict(raw_data, ['metadata_resp', 'filmstrip_url'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.mp4'), ext='mp4', identifier=video_id, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"dailymotion.com"}
        return BaseVideoClient.belongto(url, valid_domains)