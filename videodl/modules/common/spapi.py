'''
Function:
    Implementation of SpapiVideoClient: https://api.spapi.cn/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import copy
import base64
import hashlib
import json_repair
import urllib.parse
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from ..utils.domains import platformfromurl
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, safeextractfromdict


'''SpapiVideoClient'''
class SpapiVideoClient(BaseVideoClient):
    source = 'SpapiVideoClient'
    def __init__(self, **kwargs):
        super(SpapiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", "Content-Type": "text/plain", "Origin": "https://spapi.cn", "Referer": "https://spapi.cn/"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getdynamicconfig'''
    def _getdynamicconfig(self, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"', "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "cache-control": "max-age=0", "referer": "https://www.i3zh.com/", 
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "cross-site", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36", "connection": "keep-alive", "host": "api.spapi.cn", 
        }
        try:
            (resp := self.get("https://spapi.cn/dsp.html", headers=headers, timeout=10, **request_overrides)).raise_for_status()
            if (match := re.search(r'window\.__SPAPIAPP__\s*=\s*[\'"]([^\'"]+)[\'"]', resp.text)): return json_repair.loads(urllib.parse.unquote(match.group(1)))
        except Exception:
            return {'pathURL': 'YXBpL2h0bWw=', 'baseURL': 'Ly9hcGkuc3BhcGkuY24v'}
    '''_evpbytestokey'''
    def _evpbytestokey(self, password, salt, key_len, iv_len):
        d = d_i = b''
        while len(d) < key_len + iv_len: d_i = hashlib.md5(d_i + password + salt).digest(); d += d_i
        return d[:key_len], d[key_len: key_len+iv_len]
    '''_cryptojsaesencrypt'''
    def _cryptojsaesencrypt(self, plaintext: str, passphrase: str):
        key, iv = self._evpbytestokey(passphrase.encode('utf-8'), (salt := get_random_bytes(8)), 32, 16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        return base64.b64encode(b"Salted__" + salt + ciphertext).decode('utf-8')
    '''_cryptojsaesdecrypt'''
    def _cryptojsaesdecrypt(self, encrypted_payload: str, passphrase: str):
        encrypted_bytes = base64.b64decode(encrypted_payload)
        salt, ciphertext = encrypted_bytes[8: 16], encrypted_bytes[16:]
        key, iv = self._evpbytestokey(passphrase.encode('utf-8'), salt, 32, 16)
        cipher = AES.new(key, AES.MODE_CBC, iv); decrypted_padded = cipher.decrypt(ciphertext)
        return unpad(decrypted_padded, AES.block_size).decode('utf-8')
    '''_getdynamicaeskey'''
    def _getdynamicaeskey(self, cookie_val):
        huge_string = "U2FsdGVkX1/6CENRp9nWPOIU5OT7vZrK4ps2PZyFCwHG/pDBiLGNEWYBde36TJEYrXZOFhWj0QBx5TK45pPkaeKpNmkB0AsGJbWuPOO1s8cxafanPniFNNWKay4dygi9k2zXu1by+i7mEkz1kr6KAG+vpAk53Xb8J7TgxJKCojspqfoFe4iy8rtUG6tTRdTqkqs7TqW/TtAJehb0SUcKi0DbCvD3uTtSP1WOa912xN7hSnFg6/c7AElOEYxW4SUMAAxcsh3EZ/ao9daScmpFgzyri9xw2Wmb2/ggXqKyeXbgAyyyHn/wvizG/+f7mLmHq1swgzN4t68Qn2McsQOOVbE1ws/0p1Tiz+U4Mfx/x3k4fiTcKlc88uNGuZCqcMTOuZyHgU/PopNKOVaoMaqO+qbYHMS9zrdeQOIo1Jm+jgbPcgZUeq76CdCY+bbkbEF3vAkvfkjUDJEtB88yr8t0u/HwupWXKTsgGT/vExOShbTSvKL66U8fyMRj9REkmWUoETmBbguOtw2GngcN1KQt1KzUnNpQ8wHe3b+oJrjahTDdja70VQJYWMz/No9bQA4torbwPQKlZgPLDBN6kcuF5YrENq2e5udPwNc/RZU8aalT71E+qzleBQoi2P7iJXBiHle9Qls+gTtkP+RxBjsX9szMkvlrufM/FjjC/yxUsFf0Igwqgryzs4Yu2pZL+jiGYelpF3FiEaC3mIa8ybNNBUKYM2X516bO3mN1IvT2WUg1Vpx4o+STV0svMn9dkzA/cWxMYUteM0jmERAY9SJ6Degedm9xclha2cBB1IloddweGmDAy+PlEGPuhamDBFcgxkrlEc1IpqUvxhwLYBqJ8Vbxb00P4dSimWS9lRC2D1KkkPnWP9ngb/3OqnMWYBscBJvnbx7JYr9kpGeBHHmxY9azO0BT/qRbMaWJBtyMvpSOVxfTpBeEeVrrKT5yDaNafaWJwAaOpNvB+Ur96gm9iqzwSiqnU6x5UgM+ANJ4MREycLTl2MQdfIO7B4JVh8bLrLy1EceLbEMDl/j1jKRhYaA/2aEhFthxl5giluF599vJEZbqTLN+gp41twelsN68ag0ceB70OZk3N2SlAfJPUnFIBcbNQQrNazU6BsE98ux7AkHbPgikPPTYviJEAjxwvv/Q/majYjKwZyXSD1SocdRn3wcoTWG78SzwWRTqP5LqTEQK6M/h2nAEvjVA14o196heq1DhscNWa39cXMqsuA=="
        rsa_priv_text = self._cryptojsaesdecrypt(huge_string, "kfapicn")
        clean_b64 = re.sub(r'-----.*?-----', '', rsa_priv_text); clean_b64 = re.sub(r'\s+', '', clean_b64); der_bytes = base64.b64decode(clean_b64)
        rsakey = RSA.import_key(der_bytes); cipher = Cipher_PKCS1_v1_5.new(rsakey); ciphertext = base64.b64decode(urllib.parse.unquote(cookie_val))
        sentinel = get_random_bytes(16); decrypted_bytes = cipher.decrypt(ciphertext, sentinel)
        return decrypted_bytes.decode('utf-8')
    '''_safeencrypt'''
    def _safeencrypt(self, plaintext, cookie_val, default_key):
        if cookie_val:
            try: return self._cryptojsaesencrypt(plaintext, self._getdynamicaeskey(cookie_val))
            except Exception: pass
        return self._cryptojsaesencrypt(plaintext, default_key)
    '''_safedecrypt'''
    def _safedecrypt(self, res_text, cookie_val, default_key):
        if cookie_val:
            try: return self._cryptojsaesdecrypt(res_text, self._getdynamicaeskey(cookie_val))
            except Exception: pass
        return self._cryptojsaesdecrypt(res_text, default_key)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        request_overrides, null_backup_title, video_infos = request_overrides or {}, yieldtimerelatedtitle(self.source), []
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://weibo.com/'}))
        # try parse
        try:
            # --post request first time
            config = self._getdynamicconfig(request_overrides=request_overrides)
            base_url = base64.b64decode(config['baseURL']).decode('utf-8'); path_url = base64.b64decode(config['pathURL']).decode('utf-8'); api_url = f"https:{base_url}{path_url}"
            timestamp, action, md5_salt = int(time.time()), "analyze", "0SX1mOg9"; t_hex = "0x" + format(timestamp, 'x'); sign_str = f"{action}{t_hex}{md5_salt}"
            params = {"d": action, "t": timestamp, "s": hashlib.md5(sign_str.encode('utf-8')).hexdigest()}; payload = self._cryptojsaesencrypt(url, "kfapicn")
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            (resp := self.post(api_url, headers=headers, params=params, data=payload, **request_overrides)).raise_for_status(); cookies = resp.cookies
            # --post request second time
            kfapi_appkey = cookies.get('KFAPI_APPKEY'); payload = self._safeencrypt(url, kfapi_appkey, "kfapicn")
            timestamp = int(time.time()); t_hex = "0x" + format(timestamp, 'x'); sign = hashlib.md5(f"{action}{t_hex}{md5_salt}".encode('utf-8')).hexdigest()
            (resp := self.post(api_url, headers=headers, params={"d": action, "t": timestamp, "s": sign}, data=payload, cookies=cookies, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(self._safedecrypt(resp.text, kfapi_appkey, "kfapicn")))))
            # --video title
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            video_info.update(dict(download_url=(safeextractfromdict(raw_data, ['data', 'video'], None) or raw_data['data']['url'])))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=safeextractfromdict(raw_data, ['data', 'image'], None))); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos