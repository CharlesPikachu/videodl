'''
Function:
    Implementation of ChinaDailyVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import html
from .base import BaseVideoClient
from urllib.parse import urlparse, urlsplit, parse_qs, unquote
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''ChinaDailyVideoClient'''
class ChinaDailyVideoClient(BaseVideoClient):
    source = 'ChinaDailyVideoClient'
    def __init__(self, **kwargs):
        super(ChinaDailyVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, text: str) -> dict:
        video_url, cover_url, title = "", "", ""
        iframe_src = m.group(1) if (m := re.search(r'<iframe\b[^>]*\bsrc="([^"]+)"', (text := html.unescape(text)), re.I | re.S)) else ""
        if iframe_src: video_url = (qs := parse_qs(urlsplit(iframe_src).query)).get("src", [""])[0]; cover_url = qs.get("p", [""])[0]; title = unquote(qs.get("t", [""])[0])
        if not title: title = m.group(1) if (m := re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', text, re.I)) else title
        if not title: title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if (m := re.search(r'<h1[^>]*>(.*?)</h1>', text, re.I | re.S)) else title
        if not cover_url: cover_url = m.group(1) if (m := re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', text, re.I)) else cover_url
        return {"video_url": "https:" + video_url if video_url.startswith("//") else video_url, "title": html.unescape(title).replace("\xa0", " ").strip(), "cover_url": "https:" + cover_url if cover_url.startswith("//") else cover_url}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url=url).path.strip('/').split('/')[-1].removesuffix('.html').removesuffix('.htm')
            (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := self._extractvideoinfo(resp.text)))); video_info.update(dict(download_url=raw_data['video_url']))
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=raw_data.get('cover_url')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"chinadaily.com.cn"}
        return BaseVideoClient.belongto(url, valid_domains)