'''
Function:
    Implementation of BaiduTiebaVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, ensureplaywrightchromium, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


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
        from playwright.sync_api import sync_playwright
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
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        self.default_headers['Cookie'], video_infos = self._getcookies() if not self.default_headers.get('Cookie') else self.default_headers.get('Cookie'), []
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")
            # --video title
            title_tag = soup.select_one("h3.core_title_txt")
            if title_tag: video_title = (title_tag.get("title") or title_tag.get_text(strip=True)).strip()
            elif soup.title: video_title = soup.title.get_text(strip=True)
            else: video_title = null_backup_title
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download urls
            for _, tag in enumerate(soup.find_all(attrs={"data-video": True})):
                download_url = tag.get("data-video")
                if not download_url: continue
                download_url = download_url.strip()
                per_video_title = tag.get("data-title") or tag.get("title") or video_title or null_backup_title
                per_video_title = per_video_title if len(soup.find_all(attrs={"data-video": True})) == 1 else f'ep{len(video_infos)+1}-{per_video_title}'
                per_video_title = legalizestring(per_video_title, replace_null_string=null_backup_title).removesuffix('.')
                video_page_info = copy.deepcopy(video_info)
                video_page_info.update(dict(raw_data=str(tag)))
                video_page_info.update(dict(download_url=download_url))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_page_info.update(dict(
                    title=per_video_title, file_path=os.path.join(self.work_dir, self.source, f'{per_video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=per_video_title,
                ))
                video_infos.append(video_page_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["tieba.baidu.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)