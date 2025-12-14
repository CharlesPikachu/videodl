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
import time
import base64
import hashlib
import json_repair
import urllib.parse
from datetime import datetime
from Crypto.Cipher import AES
from ..sources import BaseVideoClient
from Crypto.Util.Padding import unpad
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, resp2json


'''XMFlvVideoClient'''
class XMFlvVideoClient(BaseVideoClient):
    source = 'XMFlvVideoClient'
    def __init__(self, **kwargs):
        super(XMFlvVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://jx.xmflv.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
        }
        self.default_download_headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "origin": "https://jx.xmflv.com",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_zeropad'''
    def _zeropad(self, data: bytes, block_size: int = 16) -> bytes:
        pad_len = (-len(data)) % block_size
        if pad_len == 0:
            return data
        return data + b"\x00" * pad_len
    '''_generatekey'''
    def _generatekey(self, time_str: str, url: str) -> str:
        encoded_url = urllib.parse.quote(url, safe="")
        input_str = time_str + encoded_url
        inner_hash_hex = hashlib.md5(input_str.encode("utf-8")).hexdigest()
        key_hash_hex = hashlib.md5(inner_hash_hex.encode("utf-8")).hexdigest()
        key = key_hash_hex.encode("utf-8")
        iv = b"OrSrAd8RtISPnooc"
        data = inner_hash_hex.encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(self._zeropad(data, 16))
        return base64.b64encode(ct).decode("utf-8")
    '''_generatetoken'''
    def _generatetoken(self, key_str: str) -> str:
        xor_key_proto = "m7EgOccP4xSeyjwQ"
        xor_key = xor_key_proto.encode("utf-8")
        input_buf = key_str.encode("utf-8")
        length = len(input_buf)
        padded_len = (length + 15) >> 4 << 4
        buffer = bytearray(padded_len)
        buffer[:length] = input_buf
        if padded_len > length: buffer[length] = 0x80
        output = bytearray(padded_len)
        for i in range(padded_len): output[i] = buffer[i] ^ xor_key[i % 16]
        return base64.b64encode(bytes(output)).decode("utf-8")
    '''_decryptresp'''
    def _decryptresp(self, encrypted_data: str) -> str:
        key = b"4zYgSAsEAUS6YAud"
        iv = b"ppa7qtR4McCIMCX4"
        ct = base64.b64decode(encrypted_data)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(ct)
        pt = unpad(pt, 16)
        return pt.decode("utf-8")
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        # try parse
        video_infos = []
        try:
            # --fetch time and area
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            headers["accept"] = "*/*"
            headers["origin"] = "https://jx.xmflv.com"
            pre_resp = self.get(f"https://data.video.iqiyi.com/v.f4v?src=iqiyi.com", headers=headers, **request_overrides)
            pre_resp.raise_for_status()
            raw_data = resp2json(resp=pre_resp)
            server_time, server_area = str(raw_data.get("time")), raw_data.get("t")
            if not server_time or not server_area: raise RuntimeError("Failed to retrieve time or area from https://data.video.iqiyi.com/v.f4v?src=iqiyi.com")
            # --generate corresponding parameters
            key = self._generatekey(server_time, url)
            token = self._generatetoken(key)
            # --post to parse API
            data_json = {"ua": "0", "url": urllib.parse.quote(url, safe=""), "time": server_time, "key": key, "token": token, "area": server_area}
            resp = self.post('https://202.189.8.170/Api.js', data=data_json, headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data['API.js'] = resp2json(resp=resp)
            # --decrypt response
            decrypted_data = self._decryptresp(raw_data['API.js']['data'])
            decrypted_data = json_repair.loads(decrypted_data)
            # --video title
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(decrypted_data.get('name', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            # --download url
            download_url = decrypted_data['url']
            video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True,
                guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos