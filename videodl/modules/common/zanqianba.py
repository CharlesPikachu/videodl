'''
Function:
    Implementation ZanqianbaVideoClient: https://www.zanqianba.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import zlib
import copy
import time
import base64
import hashlib
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''ZanqianbaVideoClient'''
class ZanqianbaVideoClient(BaseVideoClient):
    source = 'ZanqianbaVideoClient'
    def __init__(self, **kwargs):
        if 'enable_curl_cffi' not in kwargs: kwargs['enable_curl_cffi'] = True
        super(ZanqianbaVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            'Cookie': 'tokens=3b1cc73dae3d0c57794a73d2a1b82ea5'
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_b64utf8'''
    def _b64utf8(self, s: str) -> str:
        return base64.b64encode(s.encode("utf-8")).decode("ascii")
    '''_gtk'''
    def _gtk(self, raw: str) -> str:
        SEED = 0x1F35
        b64 = self._b64utf8(raw)
        crc = zlib.crc32(b64.encode("utf-8")) & 0xFFFFFFFF
        parts, prev = [str(SEED << 5),], SEED
        for ch in b64:
            code = ord(ch)
            parts.append(str((prev << 5) + code))
            prev = code
        payload = "".join(parts) + str(crc)
        return hashlib.md5(payload.encode("utf-8")).hexdigest()
    '''_computes'''
    def _computes(self, link: str, t_ms: int) -> str:
        sig = self._gtk(f"{link}{t_ms}")
        return self._b64utf8(sig)
    '''_buildparams'''
    def _buildparams(self, page_url: str, token: str = "bb48e54a257215548d221ecb215663d3", user_id: str = "") -> dict:
        t_ms = int(time.time() * 1000)
        s = self._computes(page_url, t_ms)
        return {"pageUrl": page_url, "token": token, "t": t_ms, "s": s, "user_id": user_id or ""}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        null_backup_title = yieldtimerelatedtitle(self.source)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        # try parse
        video_infos = []
        try:
            # --post request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.post(f'https://www.zanqianba.com/parse/apply', headers=headers, data=self._buildparams(url), **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data['data']['data'].get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            download_url = raw_data['data']['data']['videoUrls'][0]
            video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, 
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if ext in ['bin', 'm4s']: ext = 'mp4'
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos