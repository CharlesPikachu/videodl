'''
Function:
    Implementation of MiZhiVideoClient: https://api.98dou.cn/doc/video_qsy/juhe.html
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, safeextractfromdict


'''MiZhiVideoClient'''
class MiZhiVideoClient(BaseVideoClient):
    source = 'MiZhiVideoClient'
    def __init__(self, **kwargs):
        super(MiZhiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
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
            try: (resp := self.get(f'https://api.98dou.cn/api/video_qsy/juhe?url={url}', **request_overrides)).raise_for_status()
            except: (resp := self.get(f'https://api-v2.cenguigui.cn/api/juhe/video.php?url={url}', headers=headers, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            # --video title
            video_title = legalizestring(safeextractfromdict(raw_data, ['data', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url
            video_info.update(dict(download_url=(download_url := f'https:{download_url}' if not str(download_url := raw_data['data']['url']).startswith('http') else download_url)))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            cover_url = safeextractfromdict(raw_data, ['data', 'cover'], None) or safeextractfromdict(raw_data, ['data', 'pic'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=cover_url)); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos