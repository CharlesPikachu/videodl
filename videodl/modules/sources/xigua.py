'''
Function:
    Implementation of XiguaVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import copy
import zlib
import base64
import hashlib
import itertools
import json_repair
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''XiguaVideoClient'''
class XiguaVideoClient(BaseVideoClient):
    source = 'XiguaVideoClient'
    def __init__(self, **kwargs):
        super(XiguaVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlwithsucps'''
    @useparseheaderscookies
    def _parsefromurlwithsucps(self, url: str, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            SEED = 0x1F35
            def _b64utf8(s: str) -> str: return base64.b64encode(s.encode("utf-8")).decode("ascii")
            def _gtk(raw: str) -> str: return (lambda b64: hashlib.md5(("".join([str(SEED<<5), *map(str, ((p<<5)+c for p,c in itertools.pairwise(itertools.chain([SEED], map(ord, b64)))))]) + str(zlib.crc32(b64.encode("utf-8")) & 0xFFFFFFFF)).encode("utf-8")).hexdigest())(_b64utf8(raw))
            def _computes(link: str, t_ms: int) -> str: return _b64utf8(_gtk(f"{link}{t_ms}"))
            def _buildparams(page_url: str, token: str = "bb48e54a257215548d221ecb215663d3", user_id: str = "") -> dict: t_ms=int(time.time()*1000); return {"pageUrl": page_url, "token": token, "t": t_ms, "s": _computes(page_url, t_ms), "user_id": user_id or ""}
            headers = copy.deepcopy(self.default_parse_headers)
            headers.update({'Cookie': 'tokens=bb48e54a257215548d221ecb215663d3'})
            resp = self.post('https://xigua.sucps.com/parse/apply', data=_buildparams(url), headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info = VideoInfo(source=self.source, raw_data=raw_data, download_url=raw_data['data']['data']['videoUrls'][0])
            video_title = raw_data['data']['data'].get('title') or null_backup_title
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=raw_data['data']['data']['videoUrls'][0], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid
            ))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlwithsucps >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''_parsefromurlwithmixiguadouyin'''
    @useparseheaderscookies
    def _parsefromurlwithmixiguadouyin(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('/')[-1]
            resp = self.get(f"https://m.ixigua.com/douyin/share/video/{vid}?aweme_type=107&schema_type=1&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme", **request_overrides)
            resp.raise_for_status()
            raw_data = re.findall(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>", resp.text)[0]
            raw_data = json_repair.loads(raw_data)
            video_info.update(dict(raw_data=raw_data))
            download_url = raw_data["loaderData"]["video_(id)/page"]['videoInfoRes']["item_list"][0]["video"]["play_addr"]["url_list"][0]
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data["loaderData"]["video_(id)/page"]['videoInfoRes']["item_list"][0].get('desc', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid,
            ))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlwithmixiguadouyin >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlwithsucps, self._parsefromurlwithmixiguadouyin]:
            video_infos = parser(url, request_overrides)
            if any(((info.get("download_url") or "") not in ("", "NULL")) for info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.ixigua.com", "v.ixigua.com", 'm.ixigua.com']
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)