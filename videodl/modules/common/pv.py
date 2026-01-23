'''
Function:
    Implementation of PVVideoClient: https://www.parsevideo.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import random
import struct
import base64
import hashlib
import json_repair
import urllib.parse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from ..sources import BaseVideoClient
from typing import Any, Dict, List, Tuple
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''PVVideoClient'''
class PVVideoClient(BaseVideoClient):
    source = 'PVVideoClient'
    def __init__(self, **kwargs):
        super(PVVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_buildquery'''
    def _buildquery(self, url):
        timestamp = int(time.time() * 1000)
        hash_string = f"{url}%8vcf{timestamp}"
        md5_hash = hashlib.md5(hash_string.encode()).hexdigest()
        return f"hash={md5_hash}&timestamp={timestamp}"
    '''_wordstokey'''
    def _wordstokey(self, words, sig_bytes):
        byte_array = bytearray()
        for word in words: byte_array.extend(struct.pack(">I", word & 0xFFFFFFFF))
        return bytes(byte_array[:sig_bytes])
    '''_encrypturl'''
    def _encrypturl(self, url_data: str):
        key_words = [1681142116, 946037817, 946221104, 1647456308, 1698248752, 809056568, 1701013048, 875706213]
        sig_bytes = 32
        key_bytes = self._wordstokey(key_words, sig_bytes)
        data_bytes = url_data.encode("utf-8")
        block_size = 16
        padding_length = block_size - (len(data_bytes) % block_size)
        padded_data = data_bytes + bytes([padding_length] * padding_length)
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        encrypted = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted).decode("utf-8")
    '''_parsebase64'''
    def _parsebase64(self, base64_string):
        data_bytes, words = base64.b64decode(base64_string), []
        padded_data = data_bytes.ljust((len(data_bytes) + 3) // 4 * 4, b"\x00")
        for i in range(0, len(padded_data), 4):
            word = struct.unpack(">i", padded_data[i : i + 4])[0]
            words.append(word)
        return {"words": words, "sigBytes": len(data_bytes)}
    '''_wordstohex'''
    def _wordstohex(self, word_array):
        words = word_array["words"]
        sig_bytes = word_array["sigBytes"]
        byte_array = bytearray()
        for word in words: byte_array.extend(struct.pack(">i", word))
        result_bytes = bytes(byte_array[:sig_bytes])
        hex_string = result_bytes.hex()
        return hex_string
    '''_encodeurl'''
    def _encodeurl(self, url, proxy=True):
        if isinstance(url, bytes): url = url.decode("utf-8")
        encoded = urllib.parse.quote(url, safe="")
        return f"url={encoded}{'&proxyip=on' if proxy else ''}"
    '''_decryptresponse'''
    def _decryptresponse(self, encrypted_hex, key_hex):
        key = bytes.fromhex(key_hex)
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
        decrypted_text = decrypted_bytes.decode('utf-8')
        return json_repair.loads(decrypted_text)
    '''_splitandsortformats'''
    def _splitandsortformats(self, formats: List[Dict[str, Any]], include_muxed_in_audio: bool = False) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        W_BY_H = {240:426, 360:640, 480:854, 720:1280, 1080:1920, 1440:2560, 2160:3840, 4320:7680}
        def _nonecodec(x: Any) -> bool: return (x is None) or (x == "none") or (x == "")
        def _vcodecrank(v: str) -> int: v=(v or "").lower(); return 3 if ("av01" in v or "av1" in v) else (2 if "vp9" in v else (1 if ("avc" in v or "h264" in v) else 0))
        def _acodecrank(a: str) -> int: a=(a or "").lower(); return 2 if "opus" in a else (1 if ("mp4a" in a or "aac" in a) else 0)
        def _label(f: Dict[str, Any]) -> str: return (f.get("format") or f.get("format_note") or f.get("quality") or "") or ""
        def _parsefromlabel(label: str):
            s=label.strip(); up=s.upper(); h=int(m.group(1)) if (m:=re.search(r'(\d{3,4})\s*[pP]\b', s)) else (4320 if "8K" in up else 2160 if "4K" in up else 1440 if "2K" in up else 0)
            fps=int(m.group(1)) if (m:=re.search(r'(\d{2,3})\s*(?:fps|FPS|帧)\b', s)) else (int(m.group(1)) if h>0 and (m:=re.search(r'[pP]\s*(\d{2,3})\b', s)) and 24<=int(m.group(1))<=240 else 0)
            high_br=int(any(k in s for k in ("高码率","高比特","高帧率"))); hdr_dolby=int(any(k in up for k in ("HDR","DOLBY","DV")) or ("杜比" in s) or ("真彩" in s))
            return h, fps, high_br, hdr_dolby
        def _infervideofields(f: Dict[str, Any]):
            h=f.get("height") or 0; w=f.get("width") or 0; fps=f.get("fps") or 0; high_br=hdr_dolby=0
            if (h==0 or fps==0) and (not _nonecodec(f.get("vcodec")) or _label(f)):
                ph,pfps,high_br,hdr_dolby=_parsefromlabel(_label(f)); h=ph if h==0 else h; fps=pfps if fps==0 else fps
            w = W_BY_H[h] if (w==0 and h in W_BY_H) else w
            return h, w, fps, high_br, hdr_dolby
        def _lookslikevideo(f: Dict[str, Any]) -> bool:
            if not _nonecodec(f.get("vcodec")): return True
            h, _, _, _, _ = _infervideofields(f)
            lab = _label(f).upper()
            return (h > 0) or ("HDR" in lab) or ("DOLBY" in lab) or ("DV" in lab) or ("4K" in lab) or ("8K" in lab)
        def _lookslikeaudio(f: Dict[str, Any]) -> bool:
            if not _nonecodec(f.get("acodec")) and _nonecodec(f.get("vcodec")): return True
            lab = _label(f).lower()
            return any(k in lab for k in ["audio", "aac", "opus", "mp3", "flac", "音频", "音质"])
        videos = [f for f in formats if _lookslikevideo(f)]
        audios = [f for f in formats if _lookslikeaudio(f)]
        if not videos: videos = formats
        if include_muxed_in_audio: audios += [f for f in formats if (not _nonecodec(f.get("acodec"))) and (not _nonecodec(f.get("vcodec")))]
        def _videosortkey(f: Dict[str, Any]):
            h, w, fps, high_br, hdr_dolby = _infervideofields(f)
            bitrate = f.get("vbr") or f.get("tbr")
            has_bitrate = 1 if bitrate else 0
            bitrate_val = bitrate or 0
            return (h, w, fps, has_bitrate, bitrate_val, high_br, hdr_dolby, _vcodecrank(f.get("vcodec")))
        def _audiosortkey(f: Dict[str, Any]):
            bitrate = f.get("abr") or f.get("tbr") or 0
            has_bitrate = 1 if bitrate else 0
            return (has_bitrate, bitrate, f.get("asr") or 0, f.get("audio_channels") or 0, _acodecrank(f.get("acodec")))
        videos.sort(key=_videosortkey, reverse=True)
        audios.sort(key=_audiosortkey, reverse=True)
        return videos, audios
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
            # --init
            resp = self.get('https://www.parsevideo.com/', **request_overrides)
            cookies = resp.cookies.get_dict()
            self.default_cookies.update(cookies)
            # --post request and decrypt response
            query_url = "https://www.parsevideo.com/parsevideo/enc.html?" + self._buildquery(url)
            encode_url = self._encodeurl(url)
            base64_string = self._encrypturl(encode_url)
            word_array = self._parsebase64(base64_string)
            hex_result = self._wordstohex(word_array)
            resp = self.post(query_url, data={"data": hex_result}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            raw_data = self._decryptresponse(raw_data['data'], "6434316438636439386630306232303465393830303939386563663834323765")
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --extract download urls
            video_medias, audio_medias = self._splitandsortformats(raw_data['formats'])
            if random.random() > 0.5: video_medias = [vm for vm in video_medias if 'https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/' in vm['url']][0]
            else: video_medias = [vm for vm in video_medias if 'https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/' not in vm['url']][0]
            audio_medias: dict = audio_medias[0] if audio_medias else {}
            download_url, audio_download_url = video_medias.get('url'), audio_medias.get('url')
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