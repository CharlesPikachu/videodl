'''
Function:
    Implementation of SENJiexiVideoClient: https://jiexi.789jiexi.icu:4433/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import base64
import json_repair
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, yieldtimerelatedtitle, resp2json, extracttitlefromurl


'''SENJiexiVideoClient'''
class SENJiexiVideoClient(BaseVideoClient):
    source = 'SENJiexiVideoClient'
    def __init__(self, **kwargs):
        if 'enable_curl_cffi' not in kwargs: kwargs['enable_curl_cffi'] = True
        super(SENJiexiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest", "origin": "https://jiexi.789jiexi.icu:4433", "referer": "https://jiexi.789jiexi.icu:4433/",
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_decryptvideourl'''
    def _decryptvideourl(self, encrypted_data):
        key, iv = "ARTPLAYERliUlanG".encode('utf-8'), "ArtplayerliUlanG".encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_bytes = base64.b64decode(encrypted_data)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        return unpad(decrypted_bytes, AES.block_size).decode('utf-8')
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
            # --fetch key
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.get(f'https://jiexi.789jiexi.icu:4433/jx.php?url={url}', headers=headers, **request_overrides)
            resp.raise_for_status()
            soup, target = BeautifulSoup(resp.text, "html.parser"), None
            for s in soup.find_all("script"): target: str = s.string if s.string and "var config" in s.string else target
            m = re.search(r"var\s+config\s*=\s*({.*?})\s*;", target, flags=re.S)
            raw_data = json_repair.loads(re.sub(r",\s*([}\]])", r"\1", m.group(1)))
            # --post requests
            resp = self.post("https://jiexi.789jiexi.icu:4433/api.php", data={'url': url, 'time': raw_data['time'], 'key': raw_data['key']}, headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data['api.php'] = resp2json(resp=resp)
            # --decrypt encrypted url
            raw_data['api.php']['decrypted_url'] = self._decryptvideourl(raw_data['api.php']['url'])
            raw_data['api.php']['download_url'] = self.get(raw_data['api.php']['decrypted_url'], headers=headers, allow_redirects=True, **request_overrides).url
            video_info.update(dict(raw_data=raw_data))
            video_info.update(dict(download_url=raw_data['api.php']['download_url']))
            # --video title
            video_title = legalizestring(raw_data.get('vkey') or extracttitlefromurl(url) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=raw_data['api.php']['download_url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos