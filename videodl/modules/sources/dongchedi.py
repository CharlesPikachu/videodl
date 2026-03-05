'''
Function:
    Implementation of DongchediVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import requests
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse, urlunparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, ensureplaywrightchromium, safeextractfromdict, requestsproxytoplaywright, FileTypeSniffer, VideoInfo


'''DongchediVideoClient'''
class DongchediVideoClient(BaseVideoClient):
    source = 'DongchediVideoClient'
    def __init__(self, **kwargs):
        super(DongchediVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_converttomobileurl'''
    def _converttomobileurl(self, input_url: str) -> str:
        if not input_url: return input_url
        if not input_url.startswith("http://") and not input_url.startswith("https://"): input_url = "https://" + input_url
        try:
            parsed = urlparse(input_url)
            if parsed.hostname in ("www.dongchedi.com", "dongchedi.com"): parsed = parsed._replace(netloc=parsed.netloc.replace(parsed.hostname, "m.dongchedi.com")); return urlunparse(parsed)
            return input_url
        except Exception:
            return input_url
    '''_parsefromurlusingplaywright'''
    @useparseheaderscookies
    def _parsefromurlusingplaywright(self, url: str, request_overrides: dict = None):
        # prepare
        from playwright.sync_api import sync_playwright
        ensureplaywrightchromium()
        request_overrides, url = request_overrides or {}, self._converttomobileurl(url)
        video_info, download_urls = VideoInfo(source=self.source), []
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # on response
        def handleresp_func(resp: requests.Response):
            resp_url = resp.url
            try: content_type = resp.headers.get("content-type", "")
            except Exception: content_type = ""
            if ("video" in content_type or ".mp4" in resp_url or ".m3u8" in resp_url) and (resp_url not in download_urls): download_urls.append(resp_url)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, proxy=requestsproxytoplaywright(proxy=request_overrides.get('proxies')))
                context = browser.new_context(**p.devices['iPhone 13'])
                context.set_extra_http_headers(request_overrides.get('headers') or self.default_headers or {})
                page = context.new_page(); page.on("response", handleresp_func)
                page.goto(url, wait_until="domcontentloaded"); page.wait_for_timeout(5000)
                html_content = page.content(); context.close(); browser.close()
            download_url = download_urls[0]
            soup = BeautifulSoup(html_content, 'html.parser'); script_tag = soup.find('script', id='__NEXT_DATA__')
            raw_data = json_repair.loads(script_tag.string); raw_data['sync_playwright_download_urls'] = download_urls
            video_info.update(dict(raw_data=raw_data, download_url=download_url)); video_title, cover_url = null_backup_title, None
            for program in (safeextractfromdict(raw_data, ['props', 'pageProps', 'initEpisode', 'program_list'], []) or []):
                if isinstance(program, dict) and str(program.get('unique_id_str')) == str(vid): video_title = program.get('title'); cover_url = safeextractfromdict(program, ['video_info', 'cover_url'], None)
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlusingplaywright >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlusingplaywright]:
            video_infos = parser(url, request_overrides)
            if any(((info.get("download_url") or "").upper() not in ("", "NULL")) for info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"dongchedi.com"}
        return BaseVideoClient.belongto(url, valid_domains)