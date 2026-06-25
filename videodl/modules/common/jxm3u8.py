'''
Function:
    Implementation of JXM3U8VideoClient: https://jx.m3u8.tv/jiexi/?url=
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
import base64
import hashlib
import urllib.parse
import json_repair
from Cryptodome.Cipher import AES
from ..sources import BaseVideoClient
from Cryptodome.Util.Padding import unpad
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, yieldtimerelatedtitle, resp2json, extracttitlefromurl


'''JXM3U8VideoClient'''
class JXM3U8VideoClient(BaseVideoClient):
    source = 'JXM3U8VideoClient'
    def __init__(self, **kwargs):
        super(JXM3U8VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36", "accept": "application/json, text/javascript, */*; q=0.01", "content-type": "application/x-www-form-urlencoded; charset=UTF-8", "origin": "https://jx.xmflv.com", "referer": "https://jx.xmflv.com/"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36", "origin": "https://jx.xmflv.com", "referer": "https://jx.xmflv.com/"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_decryptvideourl'''
    def _decryptvideourl(self, encrypted_data: str, key: str, iv: str) -> str:
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8')); encrypted_bytes = base64.b64decode(encrypted_data); decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return unpad(decrypted_bytes, AES.block_size).decode('utf-8')
    '''_generatekey'''
    def _generatekey(self, time_str: str, url: str) -> str:
        return hashlib.md5((str(time_str) + url).encode('utf-8')).hexdigest()
    '''_generatesign'''
    def _generatesign(self, key_str: str) -> str:
        aes_key, aes_iv, text_bytes = hashlib.md5(key_str.encode('utf-8')).hexdigest().encode('utf-8'), b'fUU9eRmkYzsgbkEK', key_str.encode('utf-8')
        if (pad_len := 16 - len(text_bytes) % 16) != 16: text_bytes += b'\x00' * pad_len
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
        return base64.b64encode(cipher.encrypt(text_bytes)).decode('utf-8')
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        request_overrides, null_backup_title, video_infos = request_overrides or {}, yieldtimerelatedtitle(self.source), []
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers=self.BILIBILI_REFERENCE_HEADERS, default_audio_download_headers=self.BILIBILI_REFERENCE_HEADERS))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers=self.WEIBO_REFERENCE_HEADERS, default_audio_download_headers=self.WEIBO_REFERENCE_HEADERS))
        # try parse
        try:
            # --generate corresponding parameters
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            time_str, encoded_url = str(int(time.time() * 1000)), urllib.parse.quote(url, safe='')
            key, sign = self._generatekey(time_str, encoded_url), self._generatesign(self._generatekey(time_str, encoded_url))
            # --post request
            (resp := self.post("https://cache.0567890.xyz:4433/Api", data={'tm': time_str, 'url': encoded_url, 'key': key, 'sign': sign}, headers=headers, **request_overrides)).raise_for_status()
            if (raw_data := {'Api': resp2json(resp=resp)})['Api'].get('code') != 200 or not raw_data['Api'].get('data'): raise RuntimeError(raw_data['Api'])
            # --decrypt encrypted url
            decrypted_str = self._decryptvideourl(raw_data['Api']['data'], raw_data['Api']['key'], raw_data['Api']['iv'])
            decrypted_data = json_repair.loads(decrypted_str[decrypted_str.find('{'):]) if '{' in decrypted_str else json_repair.loads(decrypted_str)
            decrypted_data = {k: (v.replace('\\/', '/') if isinstance(v, str) else v) for k, v in decrypted_data.items()}
            raw_data['Api']['decrypted_str'], raw_data['Api']['decrypted_data'] = decrypted_str, decrypted_data
            video_info.update(dict(raw_data=raw_data, download_url=(download_url := decrypted_data['url'])))
            # --video title
            video_title = legalizestring(decrypted_data.get('name') or extracttitlefromurl(url) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            if "解析失败啦" == video_title: raise Exception(f'Fail to parse {url}')
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if decrypted_data.get('type') in {'hls'} or '.m3u8' in download_url.lower() or '/m3u8/' in download_url.lower(): ext = 'm3u8'; guess_video_ext_result['ext'] = 'm3u8'
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=decrypted_data.get('pic'))); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos