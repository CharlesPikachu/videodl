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
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, safeextractfromdict, useparseheaderscookies, legalizestring, yieldtimerelatedtitle, resp2json, optionalimport


'''IM1907VideoClient'''
class IM1907VideoClient(BaseVideoClient):
    source = 'IM1907VideoClient'
    fancy = Style([
        ("qmark", "fg:#00d7af bold"), ("question", "bold"), ("answer", "fg:#ff5f87 bold"), ("pointer", "fg:#00d7af bold"), ("highlighted", "fg:#00d7af bold"), ("selected", "fg:#ffd75f"), 
        ("instruction", "fg:#808080"), ("disabled", "fg:#585858 italic"), ("separator", "fg:#444444"), ("text", ""), ("validation-toolbar", "fg:#ff5f5f bold"),
    ])
    def __init__(self, **kwargs):
        if ('enable_parse_curl_cffi' not in kwargs) and optionalimport('curl_cffi'): kwargs['enable_parse_curl_cffi'] = True
        super(IM1907VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://m1-z2.cloud.nnpp.vip:2223/', 'Origin': 'https://m1-z2.cloud.nnpp.vip:2223', 'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_getbeijingtime'''
    def _getbeijingtime(self):
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        beijing_time = utc_now + datetime.timedelta(hours=8)
        return beijing_time
    '''_md5encode'''
    def _md5encode(self, string: str):
        return hashlib.md5(string.encode('utf-8')).hexdigest()
    '''_calculatez'''
    def _calculatez(self, current_date: datetime.datetime):
        day = current_date.day
        val = (day + 18) ^ 10
        md5_1 = self._md5encode(str(val))
        substr = md5_1[0: 10]
        z_final = self._md5encode(substr)
        return z_final
    '''_calculates1ig'''
    def _calculates1ig(self, current_date: datetime.datetime):
        weekday_iso = current_date.isoweekday()
        js_day = 0 if weekday_iso == 7 else weekday_iso
        return js_day + 11397
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
            bj_time = self._getbeijingtime()
            z_val, s1ig_val = self._calculatez(bj_time), self._calculates1ig(bj_time)
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.get("https://m1-a1.cloud.nnpp.vip:2223/api/v/", headers=headers, params = {'z': z_val, 'jx': url, 's1ig': s1ig_val, 'g': ''}, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            for item in raw_data['data']:
                if not isinstance(item, dict): continue
                video_info_page = copy.deepcopy(video_info)
                download_url = safeextractfromdict(item, ['source', 'eps', 0, 'url'], None)
                if not download_url: continue
                video_info_page.update(dict(download_url=download_url))
                video_title = legalizestring(item.get('name') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
                ))
                video_infos.append(video_info_page)
            if len(video_infos) > 1:
                ans = questionary.checkbox("Multiple results found. Please choose the videos to download:", choices=[f'{v.title}-{v.download_url}' for v in video_infos], style=IM1907VideoClient.fancy).ask()
                video_infos = [v for v in video_infos if (f'{v.title}-{v.download_url}' in ans)]
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos