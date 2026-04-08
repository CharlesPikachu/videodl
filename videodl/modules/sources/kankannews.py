'''
Function:
    Implementation of KanKanNewsVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import html
import json_repair
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''KanKanNewsVideoClient'''
class KanKanNewsVideoClient(BaseVideoClient):
    source = 'KanKanNewsVideoClient'
    def __init__(self, **kwargs):
        super(KanKanNewsVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractfields'''
    def _extractfields(self, text):
        # init
        decode_json_string_func = lambda s: None if s is None else json_repair.loads(f'"{html.unescape(s)}"')
        first_match_func = lambda patterns, text, flags=re.S | re.I: next((m.group(1).strip() for p in patterns if (m := re.search(p, str(text), flags))), None)
        # 1) player url
        player_url = first_match_func([r'video_info\s*:\s*\{.*?play_url\s*:\s*"((?:\\.|[^"\\])*)"', r'play_url\s*:\s*"((?:\\.|[^"\\])*)"', r'["\']play_url["\']\s*:\s*["\']((?:\\.|[^"\'])*)["\']'], text)
        # 2) cover
        cover_url = first_match_func([r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', r'\bcover\s*:\s*"((?:\\.|[^"\\])*)"'], text)
        # 3) title
        title = first_match_func([r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']', r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:title["\']', r'<h1[^>]*class=["\'][^"\']*video-bt[^"\']*["\'][^>]*>(.*?)</h1>', r'<title>(.*?)</title>'], text)
        if (title := html.unescape(title).strip() if title else None) and ('_看呀STV_看看新闻网' in title): title = title.split('_')[0].strip()
        # return
        return {"player_url": decode_json_string_func(player_url), "cover_url": decode_json_string_func(cover_url), "title": title}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]; (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := self._extractfields(resp.text)), download_url=raw_data['player_url']))
            video_title = legalizestring(raw_data['title'] or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=raw_data['cover_url']))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"kankanews.com"}
        return BaseVideoClient.belongto(url, valid_domains)