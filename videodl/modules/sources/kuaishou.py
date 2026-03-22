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
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, searchdictbykey, FileTypeSniffer, VideoInfo, DrissionPageUtils


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
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            (resp := self.get(url, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'; soup = BeautifulSoup(resp.text, 'lxml')
            raw_data = json_repair.loads(re.search(r'window\.__APOLLO_STATE__\s*=\s*(\{.*?\});', str(soup), re.S).group(1))
            video_info.update(dict(raw_data=raw_data)); client: dict = raw_data["defaultClient"]
            photo_key = next((k for k, v in client.items() if isinstance(v, dict) and v.get("__typename") == "VisionVideoDetailPhoto"), "")
            photo: dict = client[photo_key]; candidates = []
            if photo.get("photoH265Url"): candidates.append({"codec": "hevc_single", "maxBitrate": 1, "resolution": 1, "url": photo["photoH265Url"], "qualityLabel": "single_hevc"})
            if photo.get("photoUrl"): candidates.append({"codec": "h264_single", "maxBitrate": 1, "resolution": 1, "url": photo["photoUrl"], "qualityLabel": "single_h264"})
            if isinstance((vr := photo.get("videoResource")), dict) and (j := (vr.get("json", {}) or {})): candidates.extend([{"codec": c, "maxBitrate": r.get("maxBitrate", 0), "resolution": r.get("width", 0) * r.get("height", 0), "url": r.get("url"), "qualityLabel": r.get("qualityLabel")} for c in ("hevc", "h264") for a in j.get(c, {}).get("adaptationSet", []) if isinstance(j.get(c), dict) and isinstance(a, dict) for r in a.get("representation", []) if isinstance(r, dict) and r.get("url")])
            codec_priority = {"hevc": 2, "hevc_single": 2, "h264": 1, "h264_single": 1}
            candidates: list[dict] = [c for c in candidates if c.get('url')]; candidates.sort(key=lambda c: (codec_priority.get(c["codec"], 0), c["maxBitrate"], c["resolution"]), reverse=True)
            video_info.update(dict(download_url=(download_url := [c["url"] for c in candidates][0])))
            video_title = legalizestring(photo.get('caption', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url[0] if (cover_url := searchdictbykey(raw_data, 'coverUrl')) else None))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlusingrequests >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''_parsefromurlusingdrissionpage'''
    @useparseheaderscookies
    def _parsefromurlusingdrissionpage(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        co_hook_func = lambda co: (co.set_argument('--disable-blink-features=AutomationControlled'), co.set_argument('--mute-audio'), co)[-1]
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            page = DrissionPageUtils.initsmartbrowser(headless=True, requests_headers=None, requests_proxies=(request_overrides.get('proxies') or self._autosetproxies()), requests_cookies=(request_overrides.get('cookies') or self.default_cookies), co_hook_func=co_hook_func)
            page.get(url); video_ele = page.ele('tag:video', timeout=10); download_url = video_ele.attr('src'); poster_ele = page.ele('xpath://*[@poster]', timeout=2)
            cover_url = poster_ele.attr('poster') if poster_ele and poster_ele.attr('poster') else None
            if (not cover_url) and (bg_ele := page.ele('.backimg-area', timeout=2)) and (style := bg_ele.attr('style')) and (match := re.search(r'url\([\'"]?(.*?)[\'"]?\)', style)): cover_url = match.group(1).replace('&amp;', '&')
            if not cover_url and (state_data := page.run_js('return window.__INITIAL_STATE__ || null;')) and (m := re.search(r"'poster': '([^']*)'", str(state_data))): cover_url = m.group(1)
            title_ele = page.ele('.video-info-title', timeout=2); video_title = title_ele.text if title_ele else page.title.replace(' - 快手', '').strip()
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.'); raw_data = page.html; page.quit()
            video_info.update(dict(raw_data=raw_data, download_url=download_url))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlusingdrissionpage >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
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