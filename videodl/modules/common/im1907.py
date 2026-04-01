'''
Function:
    Implementation of IM1907VideoClient: https://im1907.top/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import hashlib
import datetime
import questionary
from questionary import Style
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, safeextractfromdict, useparseheaderscookies, legalizestring, yieldtimerelatedtitle, resp2json


'''IM1907VideoClient'''
class IM1907VideoClient(BaseVideoClient):
    source = 'IM1907VideoClient'
    fancy = Style([
        ("qmark", "fg:#00d7af bold"), ("question", "bold"), ("answer", "fg:#ff5f87 bold"), ("pointer", "fg:#00d7af bold"), ("highlighted", "fg:#00d7af bold"), ("selected", "fg:#ffd75f"), 
        ("instruction", "fg:#808080"), ("disabled", "fg:#585858 italic"), ("separator", "fg:#444444"), ("text", ""), ("validation-toolbar", "fg:#ff5f5f bold"),
    ])
    def __init__(self, **kwargs):
        super(IM1907VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Referer': 'https://m1-z2.cloud.nnpp.vip:2223/', 'Origin': 'https://m1-z2.cloud.nnpp.vip:2223', 'Accept': 'application/json, text/javascript, */*; q=0.01'}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getbeijingtime'''
    def _getbeijingtime(self):
        return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8)
    '''_md5encode'''
    def _md5encode(self, string: str):
        return hashlib.md5(string.encode('utf-8')).hexdigest()
    '''_calculatez'''
    def _calculatez(self, current_date: datetime.datetime):
        return self._md5encode(self._md5encode(str((current_date.day + 18) ^ 10))[0: 10])
    '''_calculates1ig'''
    def _calculates1ig(self, current_date: datetime.datetime):
        return (0 if (weekday_iso := current_date.isoweekday()) == 7 else weekday_iso) + 11397
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
            bj_time = self._getbeijingtime(); z_val, s1ig_val = self._calculatez(bj_time), self._calculates1ig(bj_time)
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            (resp := self.get("https://m1-a1.cloud.nnpp.vip:2223/api/v/", headers=headers, params = {'z': z_val, 'jx': url, 's1ig': s1ig_val, 'g': ''}, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            for item in raw_data['data']:
                if (not isinstance(item, dict)) or (not (download_url := safeextractfromdict(item, ['source', 'eps', 0, 'url'], None))): continue
                (video_info_page := copy.deepcopy(video_info)).update(dict(download_url=download_url))
                video_title = legalizestring(item.get('name') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info_page.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title)); video_infos.append(video_info_page)
            if len(video_infos) > 1: ans = questionary.checkbox("Multiple results found. Please choose the videos to download:", choices=[f'{v.title}-{v.download_url}' for v in video_infos if isinstance(v, VideoInfo)], style=IM1907VideoClient.fancy).ask(); video_infos = [v for v in video_infos if isinstance(v, VideoInfo) and (f'{v.title}-{v.download_url}' in ans)]
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos