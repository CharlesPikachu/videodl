'''
Function:
    Implementation of CCTVNewsVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import hmac
import copy
import base64
import hashlib
import json_repair
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''CCTVNewsVideoClient'''
class CCTVNewsVideoClient(BaseVideoClient):
    source = 'CCTVNewsVideoClient'
    def __init__(self, **kwargs):
        super(CCTVNewsVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_generateemasheaders'''
    def _generateemasheaders(self, base_headers: dict, app_key: str, api_name: str, api_ver: str, params: dict, secret: bytes = b"emasgatewayh5"):
        query_string = "&".join([f"{k}={v}" for k, v in sorted(params.items(), key=lambda x: x[0])])
        md5_hash, timestamp = hashlib.md5(query_string.encode('utf-8')).hexdigest(), str(int(time.time()))
        sign_str = "&".join(["&&", app_key, md5_hash, timestamp, api_name, api_ver, "&&&&"])
        sign = hmac.new(secret, sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
        (base_headers := dict(base_headers)).update({"x-emas-gw-appkey": app_key, "x-emas-gw-pv": "6.1", "x-emas-gw-t": timestamp, "x-emas-gw-sign": sign, "Content-Type": "application/json; charset=utf8", "from-client": "h5"})
        return base_headers
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        # try parse
        try:
            # --send get requests
            vid = parse_qs(urlparse(url).query, keep_blank_values=True).get('item_id')[0]
            host, api_name, api_ver = "https://emas-api.cctvnews.cctv.com", "emas.feed.article.server.getArticle", "1.0.0"
            api_url, app_key, params = f"{host}/h5/{api_name}/{api_ver}", "20000009", {"articleId": vid, "appcode": "video_web"}
            request_headers = self._generateemasheaders(self.default_headers, app_key, api_name, api_ver, params)
            (resp := self.get(api_url, headers=request_headers, params=params, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(base64.b64decode(resp2json(resp=resp)['response']).decode('utf-8')))))
            # --parse videos
            for video in safeextractfromdict(raw_data, ['data', 'videos'], []):
                if not isinstance(video, dict) or not video.get('qualities'): continue
                qualities: list[dict] = sorted(video['qualities'], key=lambda item: (item.get('width'), item.get('height'), item.get('size')), reverse=True)
                (video_info_item := copy.deepcopy(video_info)).download_url = [q.get('url') for q in qualities if q.get('url') and str(q.get('url')).startswith('http')][0]
                video_title = legalizestring(video.get('title') or safeextractfromdict(raw_data, ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info_item.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
                video_info_item.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(video, ['cover', 'url'], None))); video_infos.append(video_info_item)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"cctvnews.cctv.com"}
        return BaseVideoClient.belongto(url, valid_domains)