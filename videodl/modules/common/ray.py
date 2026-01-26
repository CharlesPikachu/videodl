'''
Function:
    Implementation of RayVideoClient: https://www.raydownloader.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json
import copy
import base64
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_v1_5
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, optionalimport


'''RayVideoClient'''
class RayVideoClient(BaseVideoClient):
    source = 'RayVideoClient'
    AES_KEY = "kedou@8989!63336"
    IV_BASE64 = "a2Vkb3VAODk4OSE2MzIzMw=="
    RSA_PUBLIC_KEY_BASE64 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJZWIUIje8VjJ3okESY8stCs/a95hTUqK3fD/AST0F8mf7rTLoHCaW+AjmrqVR9NM/tvQNni67b5tGC5z3PD6oROJJ24QfcAW9urz8WjtrS/pTAfGeP/2AMCZfCu9eECidy16U2oQzBl9Q0SPoz0paJ9AfgcrHa0Zm3RVPL7JvOUzscL4AnirYImPsdaHZ52hAwz5y9bYoiWzUkuG7LvnAxO6JHQ71B3VTzM3ZmstS7wBsQ4lIbD318b49x+baaXVmC3yPW/E4Ol+OBZIBMWhzl7FgwIpgbGmsJSsqrOq3D8IgjS12K5CgkOT7EB/sil7lscgc22E5DckRpMYRG8dwIDAQAB"
    def __init__(self, **kwargs):
        if ('enable_parse_curl_cffi' not in kwargs) and optionalimport('curl_cffi'): kwargs['enable_parse_curl_cffi'] = True
        super(RayVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
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
            # --encrypt post data
            json_string = json.dumps({"url": url}, separators=(",", ":"), ensure_ascii=False)
            aes_key_bytes = self.AES_KEY.encode("utf-8")
            iv_bytes = base64.b64decode(self.IV_BASE64)
            data_bytes = json_string.encode("utf-8")
            aes_cipher = AES.new(aes_key_bytes, AES.MODE_CBC, iv_bytes)
            aes_encrypted = base64.b64encode(aes_cipher.encrypt(pad(data_bytes, AES.block_size))).decode("utf-8")
            rsa_public_key = RSA.import_key(base64.b64decode(self.RSA_PUBLIC_KEY_BASE64))
            rsa_cipher = PKCS1_v1_5.new(rsa_public_key)
            rsa_encrypted = base64.b64encode(rsa_cipher.encrypt(aes_encrypted.encode("utf-8"))).decode("utf-8")
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            # --post request
            resp = self.post('https://www.raydownloader.com/api/video/extract/v2', json=rsa_encrypted, headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --sort by quality
            data_items = raw_data["data"]["videoItemVoList"]
            video_items: list[dict] = [x for x in data_items if "baseUrl" in x and x["baseUrl"].startswith('http')]
            video_items_sorted = sorted(video_items, key=lambda item: item.get("size", 0) or 0, reverse=True)
            download_url, audio_download_url = video_items_sorted[0]['baseUrl'], video_items_sorted[0].get('audioUrl')
            video_info.update(dict(download_url=download_url))
            if audio_download_url and audio_download_url != 'NULL': video_info.update(dict(audio_download_url=audio_download_url))
            # --video title
            video_title = legalizestring(raw_data['data'].get('displayTitle', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if ext in ['txt']: raise PermissionError('The request to access rr5---sn-vgqsknld.googlevideo.com was denied.')
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=raw_data['data'].get('vid') or video_title,
            ))
            if audio_download_url and audio_download_url != 'NULL':
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                video_info.update(dict(guess_audio_ext_result=guess_audio_ext_result))
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                if audio_ext in ['m4s']: audio_ext = 'm4a'
                video_info.update(dict(audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos