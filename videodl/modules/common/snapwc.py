'''
Function:
    Implementation of SnapWCVideoClient: https://snapwc.com/zh
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import json
import base64
from ..utils import RandomIPGenerator
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asympad
from cryptography.hazmat.primitives import hashes, padding as sympad, serialization
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''SnapWCVideoClient'''
class SnapWCVideoClient(BaseVideoClient):
    source = 'SnapWCVideoClient'
    SERVER_PUBLIC_PEM = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvDU+dR2bSews55172x4L
    s/ja+Dxt9ViZcj/nY0YodYo7l4jEKtEiCNV28lpFj3CkP4HKRCjL/jYkQNKGPwVg
    gUCGr/jBF1FpDLsqa0kg+dtfkm5Xm9QAyMBeG/jPdl5BEPOVh33A1UkPO/Xw6kSH
    rfghOUwBMzRBtXeYuJiYs5sKrf+Wy5sv708TI6G4hAPJG/69W4NNFJi/ipBNxntG
    dAoUHpEy4iYsvBgiccE7U0MBDnSHSqBBtIdMMFRHARn/tc+jXaadS0a4YmhTygiN
    eAJU4QuqAE25CsvkzIYIVEmlRXVcC0afw76XcwDpKBMVR5bEPzd3tMEfA+R34L1D
    fQIDAQAB
    -----END PUBLIC KEY-----"""
    def __init__(self, **kwargs):
        if 'enable_parse_curl_cffi' not in kwargs: kwargs['enable_parse_curl_cffi'] = True
        super(SnapWCVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Content-Type": "application/json", "X-Locale": "en", "Origin": "https://snapwc.com", "Referer": "https://snapwc.com/",
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_sha256bytesofstring'''
    def _sha256bytesofstring(self, s: str) -> bytes:
        h = hashes.Hash(hashes.SHA256())
        h.update(s.encode("utf-8"))
        return h.finalize()
    '''_genclientkeypair1024'''
    def _genclientkeypair1024(self):
        priv = rsa.generate_private_key(public_exponent=65537, key_size=1024)
        priv_pem = priv.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode("utf-8")
        pub_pem = priv.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")
        return priv_pem, pub_pem
    '''_encryptrequest'''
    def _encryptrequest(self, payload: dict, server_public_pem: str, client_public_pem: str) -> dict:
        t = os.urandom(16).hex()
        key = self._sha256bytesofstring(t)
        iv = os.urandom(16)
        plaintext = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        padder = sympad.PKCS7(128).padder()
        padded = padder.update(plaintext) + padder.finalize()
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        enc = cipher.encryptor()
        ct = enc.update(padded) + enc.finalize()
        encrypted_data = base64.b64encode(iv + ct).decode("ascii")
        server_pub = serialization.load_pem_public_key(server_public_pem.encode("utf-8"))
        encrypted_key = base64.b64encode(server_pub.encrypt(t.encode("utf-8"), asympad.PKCS1v15())).decode("ascii")
        return {"encrypted_key": encrypted_key, "encrypted_data": encrypted_data, "client_public_key": client_public_pem}
    '''_decryptresponse'''
    def _decryptresponse(self, resp: dict, client_private_pem: str) -> dict:
        priv = serialization.load_pem_private_key(client_private_pem.encode("utf-8"), password=None)
        n = priv.decrypt(base64.b64decode(resp["encrypted_key"]), asympad.PKCS1v15()).decode("utf-8")
        key = self._sha256bytesofstring(n)
        raw = base64.b64decode(resp["encrypted_data"])
        iv, ct = raw[:16], raw[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        dec = cipher.decryptor()
        padded = dec.update(ct) + dec.finalize()
        unpadder = sympad.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded) + unpadder.finalize()
        return json.loads(plaintext.decode("utf-8"))
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=True)
        null_backup_title = yieldtimerelatedtitle(self.source)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        # try parse
        video_infos = []
        try:
            # --init
            client_priv_pem, client_pub_pem = self._genclientkeypair1024()
            req_body = self._encryptrequest({"url": url}, self.SERVER_PUBLIC_PEM, client_pub_pem)
            # --post request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.post(f'https://api.snapwc.com/api.parser/parse', headers=headers, json=req_body, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            raw_data = self._decryptresponse(raw_data, client_priv_pem)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            def _sortbysizedesc(items): return sorted(items, key=lambda x: (1 if int(x.get("size") or 0) == 0 else 0, -int(x.get("size") or 0)))
            if len(raw_data["videos"]) > 0 and len(raw_data["audios"]) > 0:
                raw_data["videos"], raw_data["audios"] = _sortbysizedesc(raw_data["videos"]), _sortbysizedesc(raw_data["audios"])
                download_url, audio_download_url = raw_data["videos"][0]['url'], raw_data["audios"][0]['url']
            elif len(raw_data["videos"]) > 0:
                raw_data["videos"] = _sortbysizedesc(raw_data["videos"])
                download_url, audio_download_url = raw_data["videos"][0]['url'], 'NULL'
            else:
                raw_data["muxed"] = _sortbysizedesc(raw_data["muxed"])
                download_url, audio_download_url = raw_data["muxed"][0]['url'], 'NULL'
            # --deal with special download urls
            download_url, is_converter_performed = self._convertspecialdownloadurl(download_url)
            if is_converter_performed: video_info.update(dict(enable_nm3u8dlre=True))
            video_info.update(dict(download_url=download_url))
            if audio_download_url and audio_download_url != 'NULL': video_info.update(dict(audio_download_url=audio_download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
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