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
import hashlib
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, safeextractfromdict, FileTypeSniffer, VideoInfo


'''BaiduTiebaVideoClient'''
class BaiduTiebaVideoClient(BaseVideoClient):
    source = 'BaiduTiebaVideoClient'
    SALT = "36770b1f34c9bbf2e7d1a99d2b82fa9e"
    def __init__(self, **kwargs):
        super(BaiduTiebaVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Host': 'tieba.baidu.com', 'Referer': 'https://tieba.baidu.com/'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_gettbs'''
    def _gettbs(self, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        (resp := self.get("https://tieba.baidu.com/dc/common/tbs", **request_overrides)).raise_for_status()
        return resp2json(resp=resp)['tbs']
    '''_generatesign'''
    def _generatesign(self, params: dict):
        sorted_keys = sorted((sign_params := {k: v for k, v in params.items() if k != 'sign'}).keys())
        sign_str = "".join(f"{key}={sign_params[key]}" for key in sorted_keys) + BaiduTiebaVideoClient.SALT
        (md5 := hashlib.md5()).update(sign_str.encode('utf-8'))
        return md5.hexdigest()
    '''_extractvideoitems'''
    def _extractvideoitems(self, data) -> list[dict]:
        title = safeextractfromdict(data, ['thread', 'title'], None)
        video_info = safeextractfromdict(data, ['thread', 'video_info'], {}) or {}
        results, global_cover, main_video_url = [], video_info.get("thumbnail_url", ""), video_info.get("video_url")
        if main_video_url and str(main_video_url).startswith('http'): results.append({"title": title, "cover": global_cover, "video_url": main_video_url})
        for v in (video_info.get("video_desc", []) or []):
            if (not isinstance(v, dict)) or (not (v_url := v.get("video_url"))): continue
            if any(r["video_url"] == v_url for r in results) or (not str(v_url).startswith('http')): continue
            results.append({"title": title, "cover": global_cover, "video_url": v_url})
        return results
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title, video_infos = yieldtimerelatedtitle(self.source), []
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            params = {"kz": str(vid), "pn": "1", "lz": "0", "r": "2", "mark_type": "0", "back": "0", "fr": "", "session_request_times": "1", "tbs": self._gettbs(), "subapp_type": "pc", "_client_type": "20"}
            params["sign"] = self._generatesign(params)
            (resp := self.post("https://tieba.baidu.com/c/f/pb/page_pc", params=params, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            for record in self._extractvideoitems(raw_data):
                video_title = legalizestring(record.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                (video_page_info := copy.deepcopy(video_info)).update(dict(download_url=(download_url := record.get('video_url'))))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_page_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=urlparse(download_url).path.strip('/').split('/')[-1].split('.')[0], cover_url=record.get("cover")))
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
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"tieba.baidu.com"}
        return BaseVideoClient.belongto(url, valid_domains)