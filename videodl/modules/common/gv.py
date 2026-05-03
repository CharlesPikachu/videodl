'''
Function:
    Implementation of GVVideoClient: https://greenvideo.cc/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json
import copy
import base64
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from ..sources import BaseVideoClient
from Cryptodome.Util.Padding import pad
from Cryptodome.Cipher import PKCS1_v1_5
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, safeextractfromdict


'''GVVideoClient'''
class GVVideoClient(BaseVideoClient):
    source = 'GVVideoClient'
    def __init__(self, **kwargs):
        super(GVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36", "Origin": "https://greenvideo.cc", "Referer": "https://greenvideo.cc/", "kdsystem": "GreenVideo", "Accept": "application/json, text/plain, */*"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getdynamickeys'''
    def _getdynamickeys(self, request_overrides: dict = None):
        (resp := self.get("https://greenvideo.cc/api/auth/keys", timeout=10, **(request_overrides or {}))).raise_for_status()
        return resp2json(resp=resp)['data']['k1'], resp2json(resp=resp)['data']['k2']
    '''_decryptk2withpublickey'''
    def _decryptk2withpublickey(self, k1_pem, k2_b64):
        rsa_key, c = RSA.import_key(k1_pem), int.from_bytes(base64.b64decode(k2_b64), byteorder='big')
        m_bytes = pow(c, rsa_key.e, rsa_key.n).to_bytes(rsa_key.size_in_bytes(), byteorder='big')
        aes_key = m_bytes[idx+1:].decode('utf-8') if (idx := m_bytes.find(b'\x00', 2)) != -1 else m_bytes.lstrip(b'\x00').decode('utf-8')
        return aes_key
    '''_encryptpayload'''
    def _encryptpayload(self, video_url, k1, k2):
        aes_key_str = self._decryptk2withpublickey((k1_pem := f"-----BEGIN PUBLIC KEY-----\n{k1}\n-----END PUBLIC KEY-----"), k2)
        json_string = json.dumps({"url": video_url}, separators=(",", ":"), ensure_ascii=False)
        aes_cipher = AES.new(aes_key_str.encode("utf-8"), AES.MODE_CBC, base64.b64decode("a2Vkb3VAODk4OSE2MzIzMw=="))
        aes_encrypted_str = base64.b64encode(aes_cipher.encrypt(pad(json_string.encode('utf-8'), AES.block_size))).decode("utf-8")
        rsa_cipher, data_to_encrypt, chunk_size = PKCS1_v1_5.new(RSA.import_key(k1_pem)), aes_encrypted_str.encode('utf-8'), 245
        final_encrypted_bytes = b''.join(rsa_cipher.encrypt(data_to_encrypt[i:i + chunk_size]) for i in range(0, len(data_to_encrypt), chunk_size))
        return base64.b64encode(final_encrypted_bytes).decode("utf-8")
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
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers); headers.update({"Content-Type": "application/json"})
            k1, k2 = self._getdynamickeys(request_overrides=request_overrides); encrypted_data = self._encryptpayload(url, k1, k2)
            (resp := self.post('https://greenvideo.cc/api/video/cnSimpleExtract', json=encrypted_data, headers=headers, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp)))); data_items = raw_data["data"]["videoItemVoList"]
            # --sort by quality
            video_items: list[dict] = [x for x in data_items if isinstance(x, dict) and x.get("baseUrl") and str(x["baseUrl"]).startswith('http') and ((x.get('fileType') in {"video"}) or (x.get('quality') not in {'音频', '封面'}))]
            video_items_sorted = sorted(video_items, key=lambda item: item.get("size", 0) or 0, reverse=True)
            audio_items: list[dict] = [x for x in data_items if isinstance(x, dict) and x.get("baseUrl") and str(x["baseUrl"]).startswith('http') and ((x.get('fileType') in {"audio"}) or (x.get('quality') in {'音频'}))]
            audio_items_sorted = sorted(audio_items, key=lambda item: item.get("size", 0) or 0, reverse=True)
            video_info.update(dict(download_url=(download_url := video_items_sorted[0]['baseUrl'])))
            if ((not (audio_download_url := video_items_sorted[0].get('audioUrl'))) or (not str(audio_download_url).startswith('http'))) and audio_items_sorted: audio_download_url = audio_items_sorted[0].get('baseUrl')
            if audio_download_url and str(audio_download_url).startswith('http'): video_info.update(dict(audio_download_url=audio_download_url))
            # --video title
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'displayTitle'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            try: cover_url = [x for x in data_items if isinstance(x, dict) and x.get("baseUrl") and str(x["baseUrl"]).startswith('http') and ((x.get('fileType') in {"image"}) or (x.get('quality') in {'封面'}))][0]['baseUrl']
            except Exception: cover_url = None
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=safeextractfromdict(raw_data, ['data', 'vid'], None) or video_title, cover_url=cover_url))
            if audio_download_url and str(audio_download_url).startswith('http'):
                video_info.update(dict(guess_audio_ext_result=(guess_audio_ext_result := FileTypeSniffer.getfileextensionfromurl(url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies))))
                if (audio_ext := guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']) in {'m4s', 'mp4'}: audio_ext = 'm4a'
                video_info.update(dict(audio_ext=audio_ext, audio_save_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos