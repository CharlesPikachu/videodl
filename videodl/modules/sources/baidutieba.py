'''
Function:
    Implementation of BaiduTiebaVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import copy
import time
from datetime import datetime
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from playwright.sync_api import sync_playwright
from ..utils import legalizestring, useparseheaderscookies, ensureplaywrightchromium, FileTypeSniffer


'''BaiduTiebaVideoClient'''
class BaiduTiebaVideoClient(BaseVideoClient):
    source = 'BaiduTiebaVideoClient'
    def __init__(self, **kwargs):
        super(BaiduTiebaVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Host': 'tieba.baidu.com',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getcookies'''
    def _getcookies(self):
        ensureplaywrightchromium()
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://tieba.baidu.com/", wait_until="networkidle")
            cookies = context.cookies()
            cookies_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            browser.close()
            return cookies_str
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = {}):
        # prepare
        video_info = {
            'source': self.source, 'raw_data': 'NULL', 'download_url': 'NULL', 'video_title': 'NULL', 'file_path': 'NULL', 
            'ext': 'mp4', 'download_with_ffmpeg': False,
        }
        if not self.belongto(url=url): return [video_info]
        self.default_headers['Cookie'] = self._getcookies()
        # try parse
        video_infos = []
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            title_tag = soup.select_one("h3.core_title_txt")
            if title_tag:
                video_title = (title_tag.get("title") or title_tag.get_text(strip=True)).strip()
            elif soup.title:
                video_title = soup.title.get_text(strip=True)
            else:
                video_title = f'{self.source}_null_{date_str}'
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            for tag in soup.find_all(attrs={"data-video": True}):
                download_url = tag.get("data-video")
                if not download_url: continue
                download_url = download_url.strip()
                per_video_title = tag.get("data-title") or tag.get("title") or video_title
                video_page_info = copy.deepcopy(video_info)
                video_page_info.update(dict(raw_data=tag))
                video_page_info.update(dict(download_url=download_url))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, request_overrides=request_overrides)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                if ext in ['m3u8']:
                    ext = 'mp4'
                    video_page_info.update(dict(download_with_ffmpeg=True, ext=ext))
                video_page_info.update(dict(
                    video_title=per_video_title, file_path=os.path.join(self.work_dir, self.source, per_video_title + f'.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result,
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            self.logger_handle.error(f'{self.source}.parsefromurl >>> {url} (Error: {err})', disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["tieba.baidu.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)