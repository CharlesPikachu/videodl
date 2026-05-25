'''
Function:
    Implementation of IYFVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import json
import hashlib
from .base import BaseVideoClient
from urllib.parse import urlparse, parse_qs, urlencode, quote
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, extracttitlefromurl, VideoInfo


'''IYFVideoClient'''
class IYFVideoClient(BaseVideoClient):
    source = 'IYFVideoClient'
    PLAY_VIDEO_API = "https://m10.iyf.tv/v3/video/play"
    WATCH_VIDEO_API = "https://upload.iyf.tv/api/video/play"
    def __init__(self, **kwargs):
        super(IYFVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', "Accept": "application/json, text/plain, */*", "Referer": "https://www.iyf.tv/"}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoid'''
    def _extractvideoid(self, page_url: str) -> str:
        if (m := re.search(r"/play/([^/?#]+)", page_url)): return m.group(1), 'play'
        if "v" in (qs := parse_qs(urlparse(page_url).query)) and qs["v"]: return qs["v"][0], 'watch'
    '''_extractbalancedjson'''
    def _extractbalancedjson(self, text: str, marker: str = "var injectJson =") -> dict:
        brace_start, depth, in_string, escape = text.find("{", text.find(marker)), 0, False, False
        for i in range(brace_start, len(text)):
            ch = text[i]
            if in_string: escape, in_string = (False, in_string) if escape else (ch == "\\", ch != '"'); continue
            if ch == '"': in_string = True
            elif ch == "{": depth += 1
            elif ch == "}" and (depth := depth - 1) == 0: return json.loads(text[brace_start:i + 1])
    '''_extractpconfig'''
    def _extractpconfig(self, html_text: str) -> tuple[str, str]:
        pconfig = self._extractbalancedjson(html_text)["config"][0]["pConfig"]
        return pconfig["publicKey"], pconfig["privateKey"][0]
    '''_buildsignedquery'''
    def _buildsignedquery(self, video_id: str, public_key: str, private_key: str) -> str:
        params = [("cinema", "1"), ("id", video_id), ("a", "1"), ("lang", "none"), ("usersign", "1"), ("region", "US"), ("device", "1"), ("isMasterSupport", "1")]
        raw = f"{public_key}&{(base_query := urlencode(params)).lower()}&{private_key}"
        vv = hashlib.md5(raw.encode("utf-8")).hexdigest()
        return base_query + "&vv=" + vv + "&pub=" + quote(public_key, safe="")
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid, mode = self._extractvideoid(page_url=url); (resp := self.get(url, **request_overrides)).raise_for_status()
            public_key, private_key = self._extractpconfig(resp.text); signed_query = self._buildsignedquery(vid, public_key, private_key)
            play_url = (IYFVideoClient.PLAY_VIDEO_API if mode == 'play' else IYFVideoClient.WATCH_VIDEO_API) + "?" + signed_query
            (resp := self.get(play_url, **request_overrides)).raise_for_status(); video_info.update(dict(raw_data=resp2json(resp=resp)))
            video_items: list[dict] = sorted(video_info.raw_data['data']['info'][0]['flvPathList'], key=lambda x: x['bitrate'], reverse=True)
            video_info.update(dict(download_url=video_items[0].get('result') or video_items[0].get('dashResult') or video_items[0].get('rtmp')))
            video_title = safeextractfromdict(video_info.raw_data['data']['info'][0], ['title'], None) or safeextractfromdict(video_info.raw_data['data']['info'][0], ['contxt'], None)
            if not video_title: video_title = extracttitlefromurl(url, headers=self.default_headers, cookies=self.default_cookies, request_overrides=request_overrides)
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info.ext}'), identifier=vid, cover_url=safeextractfromdict(video_info.raw_data['data']['info'][0], ['image'], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"iyf.tv"}
        return BaseVideoClient.belongto(url, valid_domains)