'''
Function:
    Implementation of JXM3U8VideoClient: https://jx.m3u8.tv/jiexi/?url=
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import base64
import urllib.parse
from Cryptodome.Cipher import AES
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, yieldtimerelatedtitle


'''JXM3U8VideoClient'''
class JXM3U8VideoClient(BaseVideoClient):
    source = 'JXM3U8VideoClient'
    def __init__(self, **kwargs):
        super(JXM3U8VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_decryptvideourl'''
    def _decryptvideourl(self, encrypted_url: str, uid: str):
        key_string, iv_string = f'2890{uid}tB959C', '2F131BE91247866E'
        key, iv = key_string.encode('utf-8'), iv_string.encode('utf-8')
        decrypted_bytes = AES.new(key, AES.MODE_CBC, iv).decrypt(base64.b64decode(encrypted_url))
        padding_len = decrypted_bytes[-1]; unpadded_bytes = decrypted_bytes[:-padding_len]
        return unpadded_bytes.decode('utf-8')
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
            # --get request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            (resp := self.get(f"https://jx.m3u8.tv/jiexi/?url={url}", headers=headers, **request_overrides)).raise_for_status(); headers.update({"Referer": f"https://jx.m3u8.tv/jiexi/?url={url}"})
            m = re.search(r'<iframe.*?src=[\'\"](.*?)[\'\"]', resp.text, re.IGNORECASE | re.DOTALL)
            if (iframe_1_url := m.group(1)).startswith('/'): iframe_1_url = urllib.parse.urljoin("https://jx.m3u8.tv", iframe_1_url)
            (resp := self.get(iframe_1_url, headers=headers, **request_overrides)).raise_for_status(); headers.update({"Referer": iframe_1_url})
            iframe_2_url = re.search(r'<iframe.*?src=[\'\"](.*?)[\'\"]', resp.text, re.IGNORECASE | re.DOTALL).group(1)
            (resp := self.get(iframe_2_url, headers=headers, **request_overrides)).raise_for_status(); headers.update({"Referer": iframe_2_url})
            m = re.search(r'<iframe.*?src=[\'\"](.*?)[\'\"]', resp.text, re.IGNORECASE | re.DOTALL)
            if (iframe_3_url := m.group(1)).startswith('/'): iframe_3_url = f"https://{urllib.parse.urlparse(iframe_2_url).netloc}{iframe_3_url}"
            (resp := self.get(iframe_3_url, headers=headers, **request_overrides)).raise_for_status(); headers.update({"Referer": iframe_3_url})
            raw_data = {'encrypted_url': re.search(r'"url"\s*:\s*"([^"]+)"', resp.text).group(1).replace('\\/', '/'), 'uid': re.search(r'"uid"\s*:\s*"([^"]+)"', resp.text).group(1)}
            raw_data['decrypted_url'] = self._decryptvideourl(raw_data['encrypted_url'], uid=raw_data['uid']); video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(urllib.parse.urlparse(raw_data['decrypted_url']).path.strip('/').split('/')[-1].removesuffix('.m3u8'), replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            video_info.update(dict(download_url=raw_data['decrypted_url']))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=None)); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos