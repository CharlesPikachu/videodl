'''
Function:
    Implementation of DongchediVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json
import base64
import random
import string
from .base import BaseVideoClient
from urllib.parse import urlparse, urlencode
from ..utils.abogus import ABogus, BrowserFingerprintGenerator
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, FileTypeSniffer, VideoInfo


'''DongchediVideoClient'''
class DongchediVideoClient(BaseVideoClient):
    source = 'DongchediVideoClient'
    UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36")
    def __init__(self, **kwargs):
        super(DongchediVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"User-Agent": DongchediVideoClient.UA, "Referer": "https://www.dongchedi.com/"}
        self.default_download_headers = {"User-Agent": DongchediVideoClient.UA, "Referer": "https://www.dongchedi.com/"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''mstoken'''
    @staticmethod
    def mstoken(n=128):
        pool = string.ascii_letters + string.digits + "-_"
        return "".join(random.choice(pool) for _ in range(n))
    '''_getcurrentvideo'''
    def _getcurrentvideo(self, group_id: str, request_overrides: dict = None) -> dict:
        html_text = self.get(f"https://www.dongchedi.com/video/{group_id}", timeout=15, **(request_overrides or {})).text
        m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.S)
        return json.loads(m.group(1))["props"]["pageProps"]["info"]
    '''_getplayauthtoken'''
    def _getplayauthtoken(self, vid: str, request_overrides: dict = None) -> str:
        params = urlencode({"aid": "1839", "app_name": "auto_web_pc", "video_id": vid, "format_type": "mp4", "watermark": "unwatermarked", "msToken": DongchediVideoClient.mstoken()})
        ab = ABogus(user_agent=DongchediVideoClient.UA, fp=BrowserFingerprintGenerator.generatefingerprint("Chrome"))
        signed = ab.generateabogus(params=params)[0]
        (resp := self.get("https://www.dongchedi.com/motor/pc/common/token?" + signed, timeout=15, **(request_overrides or {}))).raise_for_status()
        return resp2json(resp=resp)["data"]["play_auth_token"]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        video_quality_order = {"1080p": 4, "720p": 3, "540p": 2, "480p": 1, "360p": 0}
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            raw_data = self._getcurrentvideo((vid := urlparse(url).path.strip('/').split('/')[-1]), request_overrides=request_overrides)
            play_auth_token = self._getplayauthtoken(raw_data["video_info"]["vid"], request_overrides=request_overrides)
            token = json.loads(base64.b64decode(play_auth_token))["GetPlayInfoToken"]
            (resp := self.get("https://vod.bytedanceapi.com/?" + token + "&ssl=true&aid=36", headers={"User-Agent": DongchediVideoClient.UA}, timeout=15, **(request_overrides or {}))).raise_for_status()
            raw_data['download_info'] = resp2json(resp=resp); play_info_list: list[dict] = raw_data['download_info']["Result"]["Data"]["PlayInfoList"]
            outs = [(lambda u: {"definition": it.get("Definition"), "format": it.get("Format"), "size": it.get("Size"), "url": u if str(u).startswith("http") else base64.b64decode(u).decode()})(it["MainPlayUrl"] or it["BackupPlayUrl"]) for it in play_info_list]
            outs.sort(key=lambda x: video_quality_order.get(x["definition"], -1), reverse=True)
            video_info.update(dict(raw_data=raw_data, download_url=(download_url := outs[0]['url'])))
            video_title = legalizestring(safeextractfromdict(raw_data, ['title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=safeextractfromdict(raw_data, ["cover_image_info", "image_list", 0, "image_url"], None)))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlusingdrissionpage >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"dongchedi.com"}
        return BaseVideoClient.belongto(url, valid_domains)