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
from Cryptodome.Cipher import AES
from ..sources import BaseVideoClient
from Cryptodome.Util.Padding import unpad
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
            "sec-ch-ua-mobile": "?0", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "origin": "https://jx.xmflv.com", "priority": "u=1, i", "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "accept": "*/*", "sec-ch-ua-platform": "\"Windows\"", "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "cross-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_generatekey'''
    def _generatekey(self, time_str: str, url: str) -> str:
        return hashlib.md5((str(time_str) + url).encode('utf-8')).hexdigest()
    '''_generatesign'''
    def _generatesign(self, key_str: str) -> str:
        aes_key = hashlib.md5(key_str.encode('utf-8')).hexdigest().encode('utf-8'); aes_iv = b'fUU9eRmkYzsgbkEK'; text_bytes = key_str.encode('utf-8')
        if (pad_len := 16 - (len(text_bytes) % 16)) != 16: text_bytes += b'\x00' * pad_len
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv); encrypted_bytes = cipher.encrypt(text_bytes)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    '''_decryptresp'''
    def _decryptresp(self, encrypted_data: str, key: str, iv: str) -> dict:
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        decrypted_str = decrypted_bytes.decode('utf-8')
        return {k: (v.replace('\\/', '/') if isinstance(v, str) else v) for k, v in json_repair.loads(decrypted_str).items()}
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
            # --fetch time and area
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers); headers["accept"] = "*/*"; headers["origin"] = "https://jx.xmflv.com"
            (pre_resp := self.get(f"https://data.video.iqiyi.com/v.f4v?src=iqiyi.com", headers=headers, **request_overrides)).raise_for_status()
            raw_data = resp2json(resp=pre_resp); server_time, server_area = str(raw_data.get("time")), raw_data.get("t")
            if not server_time or not server_area: raise RuntimeError("Failed to retrieve time or area from https://data.video.iqiyi.com/v.f4v?src=iqiyi.com")
            # --generate corresponding parameters
            key = self._generatekey(server_time, urllib.parse.quote(url, safe="")); sign = self._generatesign(key)
            # --post to parse API
            data_json = {"tm": server_time, "url": urllib.parse.quote(url, safe=""), "key": key, "sign": sign}
            (resp := self.post('https://api.hls.one:4433/Api', data=data_json, headers=headers, **request_overrides)).raise_for_status(); raw_data['API_resp'] = resp2json(resp=resp)
            # --decrypt response
            decrypted_data = self._decryptresp(raw_data['API_resp']['data'], raw_data['API_resp']['key'], raw_data['API_resp']['iv']); raw_data['API_decrypt_resp'] = decrypted_data
            # --video title
            video_title = legalizestring(decrypted_data.get('name', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            if "解析失败啦" == video_title: raise Exception(f'Fail to parse {url}')
            # --download url
            video_info.update(dict(download_url=(download_url := decrypted_data['url'])))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=decrypted_data.get('pic'))); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos