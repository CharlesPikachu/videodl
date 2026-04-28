'''
Function:
    Implementation of MingpaoVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import html
import json_repair
from pathlib import Path
from bs4 import BeautifulSoup
from contextlib import suppress
from .base import BaseVideoClient
from urllib.parse import urlparse, urlsplit, parse_qs, urljoin, urlunsplit
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''MingpaoVideoClient'''
class MingpaoVideoClient(BaseVideoClient):
    source = 'MingpaoVideoClient'
    def __init__(self, **kwargs):
        super(MingpaoVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, html_text: str, base_url: str = "") -> dict:
        soup, videos, one_func = BeautifulSoup(html_text, "lxml"), [], lambda x: x[0] if isinstance(x, list) and x else x
        abs_url_func, file_id_func = lambda x: urljoin(base_url, x) if x else None, lambda u: Path(urlparse(str(u)).path).stem if u else None
        walk_func = lambda o: ([o] + sum((walk_func(v) for v in o.values()), []) if isinstance(o, dict) else sum((walk_func(i) for i in o), []) if isinstance(o, list) else [])
        for tag in soup.select('script[type="application/ld+json"]'):
            with suppress(Exception): data = None; data = json_repair.loads(html.unescape(tag.string or tag.get_text()))
            for item in walk_func(data):
                if "VideoObject" not in (typ if isinstance((typ := item.get("@type")), list) else [typ]): continue
                videos.append({"file_id": file_id_func((video_url := abs_url_func(one_func(item.get("contentUrl"))))), "title": one_func(item.get("name")), "cover": abs_url_func(one_func(item.get("thumbnailUrl"))), "video_url": video_url, "embed_url": abs_url_func(one_func(item.get("embedUrl")))})
        if not videos:
            title = title.get_text(strip=True) if (title := soup.select_one("h1")) else None
            cover = cover_tag.get("content") or cover_tag.get("href") if (cover_tag := soup.select_one('meta[property="og:image"], meta[name="twitter:image"], link[rel="image_src"]')) else None
            for iframe in soup.select("iframe[src]"):
                embed_url = abs_url_func(html.unescape(iframe["src"]))
                video_url = one_func(parse_qs(urlparse(embed_url).query).get("file")) or embed_url
                videos.append({"file_id": file_id_func((video_url := abs_url_func(video_url))), "title": title, "cover": abs_url_func(cover), "video_url": video_url, "embed_url": embed_url})
        return list({v["video_url"] or v["embed_url"]: v for v in videos if isinstance(v, dict) and (v.get("video_url") or v.get("embed_url"))}.values())[0]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        get_base_url_func = lambda u: (lambda p: urlunsplit((p.scheme or "https", p.netloc, "/", "", "")))(urlsplit((u := u.strip()) if "://" in u or u.startswith("//") else "https://" + u))
        # try parse
        try:
            (resp := self.get(url, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := self._extractvideoinfo(resp.text, get_base_url_func(url))), download_url=raw_data['video_url']))
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=raw_data['file_id'], cover_url=raw_data.get('cover')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"mingpao.com"}
        return BaseVideoClient.belongto(url, valid_domains)