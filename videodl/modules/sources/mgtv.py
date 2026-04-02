'''
Function:
    Implementation of MGTVVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import uuid
import base64
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils.domains import MANGO_SUFFIXES
from ..utils import legalizestring, resp2json, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, cookies2string, FileTypeSniffer, VideoInfo, DrissionPageUtils


'''MGTVVideoClient'''
class MGTVVideoClient(BaseVideoClient):
    source = 'MGTVVideoClient'
    def __init__(self, **kwargs):
        super(MGTVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        if not self.default_parse_cookies or not self.default_download_cookies: cookie_str = self._getcookies()
        if not self.default_parse_cookies: self.default_parse_headers['Cookie'] = cookie_str
        if not self.default_download_cookies: self.default_download_headers['Cookie'] = cookie_str
        self._initsession()
    '''_getcookies'''
    def _getcookies(self, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        page = DrissionPageUtils.initsmartbrowser(headless=True, requests_headers=None, requests_proxies=(request_overrides.get('proxies') or self._autosetproxies()), requests_cookies=(request_overrides.get('cookies') or self.default_cookies))
        page.get(url="https://www.mgtv.com/b/790878/23777554.html?fpa=1217&fpos=&lastp=ch_home")
        page.ele('xpath://script[contains(text(), "window.__NUXT__")]')
        cookies = DrissionPageUtils.getcookiesdict(page=page); DrissionPageUtils.quitpage(page=page)
        return cookies2string(cookies)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            # --basic information
            vid = urlparse(url).path.strip('/').split('/')[-1]; pno, did = '1030', 'e6e13014-393b-43e7-b6be-2323e4960939'
            tk2 = bytes(f'did={did}|pno={pno}|ver=0.3.0301|clit={int(time.time())}'.encode()); tk2 = base64.b64encode(tk2).decode().replace('+', '_').replace('/', '~').replace('=', '-'); tk2 = list(' '.join(tk2).split()); tk2.reverse()
            params = {'did': did, 'suuid': uuid.uuid4(), 'cxid': '', 'tk2': ''.join(tk2), 'type': 'pch5', 'video_id': vid, '_support': '10000000', 'auth_mode': '', 'src': '', 'abroad': ''}
            (resp := self.get('https://pcweb.api.mgtv.com/player/video', params=params, **request_overrides)).raise_for_status(); raw_data = resp2json(resp=resp)
            # --sources
            params = {'_support': '10000000', 'tk2': ''.join(tk2), 'pm2': raw_data['data']['atc']['pm2'], 'video_id': vid, 'type': 'pch5', 'auth_mode': '', 'src': '', 'abroad': ''}
            (resp := self.get('https://pcweb.api.mgtv.com/player/getSource', params=params, **request_overrides)).raise_for_status()
            raw_data['getSource'] = resp2json(resp=resp); video_info.update(dict(raw_data=raw_data))
            streams: list[dict] = raw_data['getSource']['data']['stream']
            streams = [s for s in streams if s.get("url")] if (self.default_cookies or request_overrides.get('cookies')) else [s for s in streams if s.get("url") and str(s.get("vip", "0")) == "0"]
            download_url = raw_data['getSource']['data']['stream_domain'][0] + max(streams, key=lambda s: int(s.get("filebitrate", 0)))['url']; video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'info', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            if guess_video_ext_result['ext'] in {'json', 'NULL', None, 'null', 'None'}:
                (resp := self.get(download_url, **request_overrides)).raise_for_status()
                video_info.update(dict(download_url=(download_url := resp2json(resp=resp)['info'])))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            cover_url = safeextractfromdict(raw_data, ['data', 'info', 'thumb'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | MANGO_SUFFIXES
        return BaseVideoClient.belongto(url, valid_domains)