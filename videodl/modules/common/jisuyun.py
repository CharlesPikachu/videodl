'''
Function:
    Implementation of JisuYunVideoClient: https://jx.2s0.cn/player/?url=
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
import json
import base64
from pathlib import PurePosixPath
from ..sources import BaseVideoClient
from urllib.parse import unquote, urlparse
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, yieldtimerelatedtitle


'''JisuYunVideoClient'''
class JisuYunVideoClient(BaseVideoClient):
    source = 'JisuYunVideoClient'
    KEY = "202512221638052109"
    def __init__(self, **kwargs):
        super(JisuYunVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/149 Safari/537.36"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/149 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_rc4decrypt'''
    def _rc4decrypt(self, enc: str, key: str) -> str:
        data, s, j, k = base64.b64decode(enc), list(range(256)), 0, key.encode()
        for i in range(256): j = (j + s[i] + k[i % len(k)]) & 255; s[i], s[j] = s[j], s[i]
        out = bytearray(); i = j = 0
        for b in data: i = (i + 1) & 255; j = (j + s[i]) & 255; s[i], s[j] = s[j], s[i]; out.append(b ^ s[(s[i] + s[j]) & 255])
        return unquote(out.decode("latin1"))
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
            # --send get request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers); headers.update({"Referer": f"https://jx.2s0.cn/player/?url={url}"})
            (resp := self.get("https://jx.2s0.cn/player/analysis.php", params={"v": url}, headers=headers, timeout=20, **request_overrides)).raise_for_status()
            raw_data = self._rc4decrypt(json.loads(re.search(r'"url"\s*:\s*(".*?")', resp.text).group(1)), JisuYunVideoClient.KEY)
            # --video title
            video_title = legalizestring(PurePosixPath(urlparse(url).path).stem or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            video_info.update(dict(raw_data=raw_data, download_url=(download_url := raw_data)))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title)); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos