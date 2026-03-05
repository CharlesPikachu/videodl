'''
Function:
    Implementation of XMFlvVideoClient: https://jx.xmflv.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import base64
import hashlib
import json_repair
import urllib.parse
from Crypto.Cipher import AES
from ..sources import BaseVideoClient
from Crypto.Util.Padding import unpad
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''XMFlvVideoClient'''
class XMFlvVideoClient(BaseVideoClient):
    source = 'XMFlvVideoClient'
    def __init__(self, **kwargs):
        super(XMFlvVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01', 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'sec-fetch-site': 'cross-site', 'pragma': 'no-cache', 
            'priority': 'u=1, i', 'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"', 'sec-ch-ua-mobile': '?0', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'origin': 'https://jx.xmflv.com', 'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0', 'cache-control': 'no-cache', 
        }
        self.default_download_headers = {
            "accept": "*/*", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://jx.xmflv.com", "priority": "u=1, i", "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "cross-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_zeropad'''
    def _zeropad(self, data: bytes, block_size: int = 16) -> bytes:
        pad_len = (-len(data)) % block_size
        if pad_len == 0: return data
        return data + b"\x00" * pad_len
    '''_generatekey'''
    def _generatekey(self, time_str: str, url: str) -> str:
        inner_hash_hex = hashlib.md5((time_str + urllib.parse.quote(url, safe="")).encode("utf-8")).hexdigest()
        key_hash_hex = hashlib.md5(inner_hash_hex.encode("utf-8")).hexdigest()
        cipher = AES.new(key_hash_hex.encode("utf-8"), AES.MODE_CBC, b"OrSrAd8RtISPnooc")
        ct = cipher.encrypt(self._zeropad(inner_hash_hex.encode("utf-8"), 16))
        return base64.b64encode(ct).decode("utf-8")
    '''_generatetoken'''
    def _generatetoken(self, key_str: str) -> str:
        xor_key = "m7EgOccP4xSeyjwQ".encode("utf-8")
        input_buf = key_str.encode("utf-8"); length = len(input_buf); padded_len = (length + 15) >> 4 << 4
        buffer = bytearray(padded_len); buffer[:length] = input_buf
        if padded_len > length: buffer[length] = 0x80
        output = bytearray(padded_len)
        for i in range(padded_len): output[i] = buffer[i] ^ xor_key[i % 16]
        return base64.b64encode(bytes(output)).decode("utf-8")
    '''_decryptresp'''
    def _decryptresp(self, encrypted_data: str) -> str:
        ct = base64.b64decode(encrypted_data)
        cipher = AES.new(b"4zYgSAsEAUS6YAud", AES.MODE_CBC, b"ppa7qtR4McCIMCX4")
        pt = cipher.decrypt(ct); pt = unpad(pt, 16)
        return pt.decode("utf-8")
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        null_backup_title = yieldtimerelatedtitle(self.source)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        # try parse
        video_infos = []
        try:
            # --fetch time and area
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            headers["accept"] = "*/*"; headers["origin"] = "https://jx.xmflv.com"
            (pre_resp := self.get(f"https://data.video.iqiyi.com/v.f4v?src=iqiyi.com", headers=headers, **request_overrides)).raise_for_status()
            raw_data = resp2json(resp=pre_resp); server_time, server_area = str(raw_data.get("time")), raw_data.get("t")
            if not server_time or not server_area: raise RuntimeError("Failed to retrieve time or area from https://data.video.iqiyi.com/v.f4v?src=iqiyi.com")
            # --generate corresponding parameters
            key = self._generatekey(server_time, url); token = self._generatetoken(key)
            # --post to parse API
            data_json = {"ua": "0", "url": urllib.parse.quote(url, safe=""), "time": server_time, "key": key, "token": token, "area": server_area}
            (resp := self.post('https://202.189.8.170/Api.js', data=data_json, headers=headers, **request_overrides)).raise_for_status()
            raw_data['API.js'] = resp2json(resp=resp)
            # --decrypt response
            decrypted_data = self._decryptresp(raw_data['API.js']['data']); decrypted_data = json_repair.loads(decrypted_data)
            raw_data['API.js']['decrypted_data'] = decrypted_data
            # --video title
            video_title = legalizestring(decrypted_data.get('name', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            if "解析失败啦" == video_title: raise Exception
            # --download url
            download_url = decrypted_data['url']; video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=decrypted_data.get('pic')))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos