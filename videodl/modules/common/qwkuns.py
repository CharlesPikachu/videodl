'''
Function:
    Implementation QwkunsVideoClient: https://qwkuns.me/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
from ..sources import BaseVideoClient
from ..utils import RandomIPGenerator
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle


'''QwkunsVideoClient'''
class QwkunsVideoClient(BaseVideoClient):
    source = 'QwkunsVideoClient'
    def __init__(self, **kwargs):
        super(QwkunsVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", "Accept": "application/json", "Content-Type": "application/json", "Origin": "https://api.qwkuns.me/"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", "Origin": "https://api.qwkuns.me/", "Accept": "*/*"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        null_backup_title = yieldtimerelatedtitle(self.source)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://weibo.com/'}))
        # try parse
        video_infos = []
        try:
            # --get request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            payload = {"url": url, "downloadMode": "auto", "filenameStyle": "basic", "disableMetadata": True, "videoQuality": "720"}
            (resp := self.post(f'https://api.qwkuns.me/', headers=headers, json=payload, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            # --video title
            video_title = legalizestring(raw_data.get('filename') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.mp4').removesuffix('.')
            # --download url
            if raw_data.get('status') in {"tunnel", "redirect"}: download_url = raw_data['url']
            else: picker_items: list[dict] = raw_data.get('picker', []) or []; download_url = next((p for p in picker_items if p.get("type") == "video"), None)['url']
            video_info.update(dict(download_url=download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            if ext in {'m4s'}: ext = 'mp4'
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=None))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos