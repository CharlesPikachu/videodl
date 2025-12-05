'''
Function:
    Implementation of KedouVideoClient: https://www.kedou.life/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json
import time
import copy
import base64
import shutil
import subprocess
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from rich.progress import Progress
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_v1_5
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, usedownloadheaderscookies


'''constants'''
RSA_PUBLIC_KEY_BASE64 = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkJZWIUIje8VjJ3okESY8stCs/a95hTUqK3fD/AST0F8mf7rTLoHCaW+AjmrqVR9NM/tvQNni67b5tGC5z3PD6oROJJ24QfcAW9urz8WjtrS/pTAfGeP/2AMCZfCu9eECidy16U2oQzBl9Q0SPoz0paJ9AfgcrHa0Zm3RVPL7JvOUzscL4AnirYImPsdaHZ52hAwz5y9bYoiWzUkuG7LvnAxO6JHQ71B3VTzM3ZmstS7wBsQ4lIbD318b49x+baaXVmC3yPW/E4Ol+OBZIBMWhzl7FgwIpgbGmsJSsqrOq3D8IgjS12K5CgkOT7EB/sil7lscgc22E5DckRpMYRG8dwIDAQAB"
AES_KEY = "kedou@8989!63336"
IV_BASE64 = "a2Vkb3VAODk4OSE2MzIzMw=="


'''KedouVideoClient'''
class KedouVideoClient(BaseVideoClient):
    source = 'KedouVideoClient'
    def __init__(self, **kwargs):
        super(KedouVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_download'''
    @usedownloadheaderscookies
    def _download(self, video_info: VideoInfo, video_info_index: int = 0, downloaded_video_infos: list = [], request_overrides: dict = None, progress: Progress | None = None):
        video_info = copy.deepcopy(video_info)
        # avoid calling ffmpeg to download audios
        audio_download_url = video_info.pop('audio_download_url')
        audio_file_path = video_info.pop('audio_file_path')
        audio_ext = video_info.pop('audio_ext')
        guess_audio_ext_result = video_info.pop('guess_audio_ext_result')
        # download videos
        super()._download(video_info=video_info, video_info_index=video_info_index, downloaded_video_infos=downloaded_video_infos, request_overrides=request_overrides, progress=progress)
        # download audios if have
        if audio_download_url and audio_download_url != 'NULL' and audio_ext in ['m4a', 'mp3', 'aac']:
            # --audio download
            audio_info = VideoInfo(
                source=self.source, download_url=audio_download_url, file_path=audio_file_path, ext=audio_ext, identifier=f'audio_{video_info["identifier"]}',
                guess_video_ext_result=guess_audio_ext_result
            )
            downloaded_audio_infos = super()._download(video_info=audio_info, video_info_index=video_info_index, downloaded_video_infos=[], request_overrides=request_overrides, progress=progress)
            assert len(downloaded_audio_infos) == 1
            audio_file_path = downloaded_audio_infos[0]['file_path']
            audio_ext = downloaded_audio_infos[0]['ext']
            # --extract video path
            tgt_dvi = [dvi for dvi in downloaded_video_infos if dvi['identifier'] == video_info["identifier"]]
            video_file_path = tgt_dvi[0]['file_path']
            # --merge
            tmp_video_file_path = os.path.join(self.work_dir, self.source, f'{int(time.time())}_{tgt_dvi[0]["identifier"]}.{tgt_dvi[0]["ext"]}')
            cmd = ['ffmpeg', '-y', '-i', video_file_path, '-i', audio_file_path, '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', tmp_video_file_path]
            capture_output = True if self.disable_print else False
            ret = subprocess.run(cmd, check=True, capture_output=capture_output, text=True, encoding='utf-8', errors='ignore')
            if ret.returncode == 0:
                shutil.move(tmp_video_file_path, video_file_path)
                if os.path.exists(audio_file_path): os.remove(audio_file_path)
            else:
                err_msg = f': {ret.stdout or ""}\n\n{ret.stderr or ""}' if capture_output else ""
                self.logger_handle.error(f'{self.source}._download >>> {video_info["download_url"]} (Error{err_msg})', disable_print=self.disable_print)
        # re append
        for dvi in downloaded_video_infos:
            if dvi['identifier'] == video_info["identifier"]:
                dvi['audio_download_url'] = audio_download_url
                dvi['audio_file_path'] = audio_file_path
                dvi['audio_ext'] = audio_ext
                dvi['guess_audio_ext_result'] = guess_audio_ext_result
        # return
        return downloaded_video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        # try parse
        video_infos = []
        try:
            # --encrypt post data
            json_string = json.dumps({"url": url}, separators=(",", ":"), ensure_ascii=False)
            aes_key_bytes = AES_KEY.encode("utf-8")
            iv_bytes = base64.b64decode(IV_BASE64)
            data_bytes = json_string.encode("utf-8")
            aes_cipher = AES.new(aes_key_bytes, AES.MODE_CBC, iv_bytes)
            aes_encrypted = base64.b64encode(aes_cipher.encrypt(pad(data_bytes, AES.block_size))).decode("utf-8")
            rsa_public_key = RSA.import_key(base64.b64decode(RSA_PUBLIC_KEY_BASE64))
            rsa_cipher = PKCS1_v1_5.new(rsa_public_key)
            rsa_encrypted = base64.b64encode(rsa_cipher.encrypt(aes_encrypted.encode("utf-8"))).decode("utf-8")
            random_ip = RandomIPGenerator().ipv4()
            headers = copy.deepcopy(self.default_headers)
            headers["X-Forwarded-For"] = random_ip
            # --post request
            resp = self.post('https://www.kedou.life/api/video/extract/v2', json=rsa_encrypted, headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --sort by quality
            data_items = raw_data["data"]["videoItemVoList"]
            video_items = [x for x in data_items if "baseUrl" in x and x["baseUrl"].startswith('http')]
            video_items_sorted = sorted(video_items, key=lambda item: item.get("size", 0) or 0, reverse=True)
            download_url, audio_download_url = video_items_sorted[0]['baseUrl'], video_items_sorted[0].get('audioUrl')
            video_info.update(dict(download_url=download_url))
            if audio_download_url and audio_download_url != 'NULL': video_info.update(dict(audio_download_url=audio_download_url))
            # --video title
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = raw_data['data'].get('displayTitle', f'{self.source}_null_{date_str}')
            video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if ext in ['txt']: raise PermissionError('The request to access rr5---sn-vgqsknld.googlevideo.com was denied.')
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=raw_data['data'].get('vid'),
            ))
            if audio_download_url and audio_download_url != 'NULL':
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                video_info.update(dict(guess_audio_ext_result=guess_audio_ext_result))
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                video_info.update(dict(audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}_audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos