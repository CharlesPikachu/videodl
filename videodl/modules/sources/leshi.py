'''
Function:
    Implementation of LeshiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import time
import base64
from functools import reduce
from .base import BaseVideoClient
from urllib.parse import urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, VideoInfo


'''LeshiVideoClient'''
class LeshiVideoClient(BaseVideoClient):
    source = 'LeshiVideoClient'
    def __init__(self, **kwargs):
        super(LeshiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Accept': '*/*', 'Referer': 'http://www.le.com/'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.le.com/'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_decryptm3u8'''
    def _decryptm3u8(self, encrypted_data: bytes):
        if encrypted_data[:5].decode('utf-8').lower() != 'vc_01': return encrypted_data
        compat_ord_func = lambda c: c if isinstance(c, int) else ord(c)
        loc4 = bytearray(2 * len((encrypted_data := encrypted_data[5:])))
        for idx, val in enumerate(encrypted_data): loc4[2 * idx] = (b := compat_ord_func(val)) // 16; loc4[2 * idx + 1] = b % 16
        idx = len(loc4) - 11; loc4 = loc4[idx:] + loc4[:idx]; loc7 = bytearray(len(encrypted_data))
        for i in range(len(encrypted_data)): loc7[i] = loc4[2 * i] * 16 + loc4[2 * i + 1]
        return bytes(loc7)
    '''_getflashurls'''
    def _getflashurls(self, media_url, request_overrides: dict = None):
        request_overrides, encode_data_uri_func = request_overrides or {}, lambda data, mime_type: f"data:{mime_type};base64,{base64.b64encode(data).decode('utf-8')}"
        for k, v in {'m3v': '1', 'format': '1', 'expect': '3', 'tss': 'ios'}.items(): media_url = re.sub(r'([?&])' + k + r'=[^&]*', r'\g<1>' + k + '=' + v, media_url) if re.search(r'([?&])' + k + r'=[^&]*', media_url) else (media_url + f"&{k}={v}")
        (resp := self.get(media_url, **request_overrides)).raise_for_status(); location_url = resp2json(resp=resp)['nodelist'][0]['location']
        (m3u8_resp := self.get(location_url, **request_overrides)).raise_for_status(); decrypted_m3u8 = self._decryptm3u8(m3u8_resp.content)
        return encode_data_uri_func(decrypted_m3u8, 'application/vnd.apple.mpegurl')
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        urshift_func = lambda val, n: (val & 0xFFFFFFFF) >> n
        ror_func = lambda param1, param2: reduce(lambda x, _: urshift_func(x, 1) + ((x & 1) << 31), range(param2), param1)
        calc_time_key_func = lambda param1: ror_func(param1, 185025305 % 17) ^ 185025305
        # try parse
        try:
            vid = m.group('id') if (m := re.search(r'https?://(?:www\.le\.com/ptv/vplay|(?:sports\.le|(?:www\.)?lesports)\.com/(?:match|video))/(?P<id>\d+)\.html', url)) else urlparse(url).path.strip('/').split('/')[-1].removesuffix('.html').removesuffix('.htm')
            (resp := self.get(f'http://player-pc.le.com/mms/out/video/playJson?{f"id={vid}&platid=1&splatid=105&format=1&source=1000&tkey={calc_time_key_func(int(time.time()))}&domain=www.le.com&region=cn"}', **request_overrides)).raise_for_status()
            video_info.update(raw_data=(raw_data := resp2json(resp=resp)))
            play_domain = safeextractfromdict(raw_data, ['msgs', 'playurl', 'domain', 0], None) or ['http://play.g3proxy.lecloud.com', 'http://bplay.g3proxy.lecloud.com', 'http://101.236.15.230'][0]
            for _, format_data in sorted(dict(raw_data['msgs']['playurl']['dispatch']).items(), key=lambda x: int(''.join(filter(str.isdigit, x[0]))), reverse=True):
                try: download_url = self._getflashurls(play_domain + format_data[0], request_overrides); break
                except Exception: continue
            video_title = legalizestring(safeextractfromdict(raw_data, ['msgs', 'playurl', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(download_url=(download_url := self._convertspecialdownloadurl(download_url)[0])))
            cover_url = safeextractfromdict(raw_data, ['msgs', 'playurl', 'picAll', '640*320'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{video_info.ext}'), identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"le.com"}
        return BaseVideoClient.belongto(url, valid_domains)