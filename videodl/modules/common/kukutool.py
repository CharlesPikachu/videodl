'''
Function:
    Implementation of KuKuToolVideoClient: https://dy.kukutool.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import time
import json
import base64
import random
import hashlib
from Cryptodome.Cipher import AES
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from Cryptodome.Util.Padding import unpad
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, safeextractfromdict


'''KuKuToolVideoClient'''
class KuKuToolVideoClient(BaseVideoClient):
    source = 'KuKuToolVideoClient'
    KEY = "12345678901234567890123456789013"
    STANDARD_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    CUSTOM_B64   = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw9876543210-_"
    def __init__(self, **kwargs):
        super(KuKuToolVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "host": "dy.kukutool.com", "origin": "https://dy.kukutool.com", "sec-ch-ua": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"", "sec-ch-ua-mobile": "?0", "connection": "keep-alive", "content-length": "212", 
            "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "accept": "*/*", "accept-encoding": "gzip, deflate, br, zstd", "referer": "https://dy.kukutool.com/xiaohongshu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", "content-type": "application/json", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", 
        }
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getparams'''
    def _getparams(self, url, secret_key="5Q0NvQxD0zdQ5RLQy5xs"):
        params = {"requestURL": url, "captchaKey": "", "captchaInput": ""}
        salt = "".join(random.choices("0123456789abcdefghijklmnopqrstuvwxyz", k=8))
        signature = self._calcsign(params, salt, (current_timestamp := int(time.time())), secret_key)
        return {**params, "ts": current_timestamp, "salt": salt, "sign": signature}
    '''_calcsign'''
    def _calcsign(self, params: dict, salt, timestamp, secret_key):
        sorted_keys = sorted(params.keys())
        param_string = "&".join([f"{key}={params[key]}" for key in sorted_keys])
        sign_str = f"{param_string}&salt={salt}&ts={timestamp}&secret={secret_key}"
        hash = hashlib.md5(sign_str.encode()).hexdigest()
        return hash.replace("b", "#").replace("d", "b").replace("#", "d")
    '''_xorstring'''
    def _xorstring(self, s: str, key: int = 0x5A) -> str:
        return "".join(chr(ord(ch) ^ key) for ch in s)
    '''_blockreverse'''
    def _blockreverse(self, s: str, block_size: int = 8) -> str:
        return "".join(s[i:i + block_size][::-1] for i in range(0, len(s), block_size))
    '''_base64customdecode'''
    def _base64customdecode(self, s: str) -> str:
        return "".join(self.STANDARD_B64[idx] if (idx := self.CUSTOM_B64.find(ch)) != -1 else ch for ch in s)
    '''_aesdecrypt'''
    def _aesdecrypt(self, data_b64_str: str, iv_b64_str: str, key_str: str):
        cipher_bytes = base64.b64decode(data_b64_str); iv_bytes = base64.b64decode(iv_b64_str); key_bytes = key_str.encode("utf-8")
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes); plain_padded = cipher.decrypt(cipher_bytes); plain = unpad(plain_padded, AES.block_size)
        return json.loads(plain.decode("utf-8"))
    '''_kukudemethodpy'''
    def _kukudemethodpy(self, data: str, iv: str, key: str) -> dict:
        # 1) XOR
        data_x = self._xorstring(data); iv_x = self._xorstring(iv)
        # 2) blockReverse
        data_r = self._blockreverse(data_x); iv_r = self._blockreverse(iv_x)
        # 3) base64CustomDecode
        data_m = self._base64customdecode(data_r); iv_m = self._base64customdecode(iv_r)
        # 4) AES-CBC
        return self._aesdecrypt(data_m, iv_m, key)
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
            # --post request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            (resp := self.post(f'https://dy.kukutool.com/api/parse', json=self._getparams(url), headers=headers, **request_overrides)).raise_for_status()
            raw_data = resp2json(resp=resp); video_info.update(dict(raw_data=(raw_data := self._kukudemethodpy(raw_data["data"], raw_data["iv"], self.KEY))))
            # --video title
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            video_info.update(dict(download_url=raw_data['url']))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['cover'], None) or safeextractfromdict(raw_data, ['pics', 0], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=cover_url)); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos