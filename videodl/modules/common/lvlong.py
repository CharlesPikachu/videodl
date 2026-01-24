'''
Function:
    Implementation of LvlongVideoClient: https://jcy.lvlong.xyz/jxr.php
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
from ..sources import BaseVideoClient
from urllib.parse import urlparse, parse_qs
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, yieldtimerelatedtitle, resp2json, touchdir


'''LvlongVideoClient'''
class LvlongVideoClient(BaseVideoClient):
    source = 'LvlongVideoClient'
    def __init__(self, **kwargs):
        super(LvlongVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
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
            # --get download url
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.get(f"https://jcy.lvlong.xyz/jxr.php?url={url}", headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            vid = parse_qs(urlparse(raw_data['video2']).query, keep_blank_values=True).get('h')[0]
            resp = self.get(raw_data['video2'], headers=headers, **request_overrides)
            resp.raise_for_status()
            video_url = re.compile(r'(?m)^\s*var\s+videoUrl\s*=\s*([\'"])(.*?)\1\s*;').search(resp.text).group(2)
            video_url = f'https://api.s01s.cn/API/Sp_jx/{video_url}'
            resp = self.get(video_url, **request_overrides)
            download_url = os.path.join(self.work_dir, self.source, f'{vid}.m3u8')
            touchdir(os.path.dirname(download_url))
            with open(download_url, "w", encoding="utf-8") as fp: fp.write(resp.text)
            assert '#EXTM3U' in resp.text and 'https://' in resp.text
            video_info.update(dict(download_url=download_url))
            # --video title
            video_title = legalizestring(raw_data.get('name') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
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