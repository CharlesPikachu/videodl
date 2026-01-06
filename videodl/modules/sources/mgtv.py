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
from ..utils import legalizestring, resp2json, useparseheaderscookies, ensureplaywrightchromium, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''MGTVVideoClient'''
class MGTVVideoClient(BaseVideoClient):
    source = 'MGTVVideoClient'
    def __init__(self, **kwargs):
        super(MGTVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        if not self.default_cookies:
            cookie_str = self._getcookies()
            self.default_parse_headers['Cookie'] = cookie_str
            self.default_download_headers['Cookie'] = cookie_str
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getcookies'''
    def _getcookies(self):
        from playwright.sync_api import sync_playwright
        ensureplaywrightchromium()
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(
                extra_http_headers=self.default_headers
            )
            page = context.new_page()
            page.goto("https://www.mgtv.com/b/790878/23777554.html?fpa=1217&fpos=&lastp=ch_home", wait_until="networkidle")
            cookies = context.cookies()
            cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            browser.close()
            return cookies_str
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
            # --basic information
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            pno, did = '1030', 'e6e13014-393b-43e7-b6be-2323e4960939'
            tk2 = bytes(f'did={did}|pno={pno}|ver=0.3.0301|clit={int(time.time())}'.encode())
            tk2 = base64.b64encode(tk2).decode().replace('/\+/g', '_').replace('/\//g', '~').replace('/=/g', '-')
            tk2 = list(' '.join(tk2).split())
            tk2.reverse()
            params = {
                'did': did, 'suuid': uuid.uuid4(), 'cxid': '', 'tk2': ''.join(tk2), 'type': 'pch5', 'video_id': vid, '_support': '10000000', 'auth_mode': '', 'src': '', 'abroad': '',
            }
            resp = self.get('https://pcweb.api.mgtv.com/player/video', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            # --sources
            pm2 = raw_data['data']['atc']['pm2']
            params = {
                '_support': '10000000', 'tk2': ''.join(tk2), 'pm2': pm2, 'video_id': vid, 'type': 'pch5', 'auth_mode': '', 'src': '', 'abroad': '',
            }
            resp = self.get('https://pcweb.api.mgtv.com/player/getSource', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data['getSource'] = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            streams = raw_data['getSource']['data']['stream']
            streams = [s for s in streams if s.get("url")] if self.default_cookies or 'cookies' in request_overrides else [s for s in streams if s.get("url") and str(s.get("vip", "0")) == "0"]
            download_url = raw_data['getSource']['data']['stream_domain'][0] + max(streams, key=lambda s: int(s.get("filebitrate", 0)))['url']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data["data"]["info"].get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if ext in ['json']:
                resp = self.get(download_url, **request_overrides)
                resp.raise_for_status()
                download_url = resp2json(resp=resp)['info']
                video_info.update(dict(download_url=download_url))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid
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
            valid_domains = ["www.mgtv.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)