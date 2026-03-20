'''
Function:
    Implementation of KuaishouVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, searchdictbykey, safeextractfromdict, FileTypeSniffer, VideoInfo, DrissionPageUtils


'''KuaishouVideoClient'''
class KuaishouVideoClient(BaseVideoClient):
    source = 'KuaishouVideoClient'
    def __init__(self, **kwargs):
        super(KuaishouVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Referer': 'https://v.kuaishou.com/'}
        self.default_download_headers = {}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlusingrequests'''
    @useparseheaderscookies
    def _parsefromurlusingrequests(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            (resp := self.get(url, **request_overrides)).raise_for_status()
            resp.encoding = 'utf-8'; soup = BeautifulSoup(resp.text, 'lxml')
            raw_data = json_repair.loads(re.search(r'window\.__APOLLO_STATE__\s*=\s*(\{.*?\});', str(soup), re.S).group(1))
            video_info.update(dict(raw_data=raw_data)); client: dict = raw_data["defaultClient"]
            photo_key = next((k for k, v in client.items() if isinstance(v, dict) and v.get("__typename") == "VisionVideoDetailPhoto"), "")
            photo: dict = client[photo_key]; candidates = []
            if photo.get("photoH265Url"): candidates.append({"codec": "hevc_single", "maxBitrate": 1, "resolution": 1, "url": photo["photoH265Url"], "qualityLabel": "single_hevc"})
            if photo.get("photoUrl"): candidates.append({"codec": "h264_single", "maxBitrate": 1, "resolution": 1, "url": photo["photoUrl"], "qualityLabel": "single_h264"})
            if isinstance((vr := photo.get("videoResource")), dict) and (j := (vr.get("json", {}) or {})): candidates.extend([{"codec": c, "maxBitrate": r.get("maxBitrate", 0), "resolution": r.get("width", 0) * r.get("height", 0), "url": r.get("url"), "qualityLabel": r.get("qualityLabel")} for c in ("hevc", "h264") for a in j.get(c, {}).get("adaptationSet", []) if isinstance(j.get(c), dict) and isinstance(a, dict) for r in a.get("representation", []) if isinstance(r, dict) and r.get("url")])
            codec_priority = {"hevc": 2, "hevc_single": 2, "h264": 1, "h264_single": 1}
            candidates: list[dict] = [c for c in candidates if c.get('url')]
            candidates.sort(key=lambda c: (codec_priority.get(c["codec"], 0), c["maxBitrate"], c["resolution"]), reverse=True)
            video_info.update(dict(download_url=(download_url := [c["url"] for c in candidates][0])))
            video_title = legalizestring(photo.get('caption', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = searchdictbykey(raw_data, 'coverUrl')
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url[0] if cover_url else None))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlusingrequests >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''_parsefromurlusingdrissionpage'''
    @useparseheaderscookies
    def _parsefromurlusingdrissionpage(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            page = DrissionPageUtils.initsmartbrowser(headless=True, requests_headers={"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}, requests_proxies=(request_overrides.get('proxies') or self._autosetproxies()), requests_cookies=(request_overrides.get('cookies') or self.default_cookies))
            page.set.window.size(390, 844); page.get(url=url); page.ele('xpath://script[contains(text(), "window.INIT_STATE")]', timeout=10); html_content = page.html; page.quit()
            t = next((s.get_text() for s in BeautifulSoup(html_content, "html.parser").find_all("script") if "window.INIT_STATE" in s.get_text()), "")
            i = t.find("window.INIT_STATE"); s = t.find("{", i); d = q = e = 0
            q_, e_, d_ = [q], [e], [d]; _j = next((j for j, ch in enumerate(t[s:], s) if not (((e_.__setitem__(0, (not e_[0] and ch == "\\")), q_.__setitem__(0, not (q_[0] and not e_[0] and ch == '"')), True)[-1]) if q_[0] else ((q_.__setitem__(0, 1), False)[-1]) if ch == '"' else ((d_.__setitem__(0, d_[0] + 1), False)[-1]) if ch == '{' else ((d_.__setitem__(0, d_[0] - 1), False)[-1]) if ch == '}' else False) and d_[0] == 0 and j >= s), None); raw_data = json_repair.loads(t[s:_j+1]) if _j is not None else raw_data; q, e, d = q_[0], e_[0], d_[0]
            video_info.update(dict(raw_data=raw_data)); formats = sorted(searchdictbykey(raw_data, 'adaptationSet')[0][0]['representation'], key=lambda x: (x.get('height', 0) * x.get('width', 0), x.get('fileSize', 0)), reverse=True)
            formats = [f for f in formats if isinstance(f, dict) and (f.get('url') or f.get('backupUrl'))]; download_url = formats[0]['url'] or formats[0]['backupUrl']
            if isinstance(download_url, list): download_url = download_url[0]
            video_title = searchdictbykey(raw_data, 'caption') or null_backup_title
            if isinstance(video_title, list): video_title = video_title[0]
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.'); video_info.update(dict(download_url=download_url))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = searchdictbykey(raw_data, 'coverUrls') or searchdictbykey(raw_data, 'webpCoverUrls')
            if cover_url: cover_url = safeextractfromdict(cover_url[0], [0, 'url'], None)
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlusingdrissionpage >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlusingdrissionpage, self._parsefromurlusingrequests]:
            video_infos = parser(url, request_overrides)
            if any(((info.get("download_url") or "").upper() not in ("", "NULL")) for info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"kuaishou.com"}
        return BaseVideoClient.belongto(url, valid_domains)