'''
Function:
    Implementation of CCtalkVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import copy
from contextlib import suppress
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, safeextractfromdict, taskprogress, FileTypeSniffer, VideoInfo


'''CCtalkVideoClient'''
class CCtalkVideoClient(BaseVideoClient):
    source = 'CCtalkVideoClient'
    def __init__(self, **kwargs):
        super(CCtalkVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36", "sec-ch-ua-mobile": "?0", "harmony-os": "pcweb", "host": "www.cctalk.com", "sec-fetch-site": "same-origin", "hujiang-app-key": "pcweb", 
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"', "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "referer": "https://www.cctalk.com/v/17604950351552?sid=1760494906733025", 
        }
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        # try parse
        try:
            # --fetch video ids
            sid = parse_qs((parsed_url := urlparse(url)).query, keep_blank_values=True).get('sid', [None])[0]
            if not sid: video_ids = [parsed_url.path.strip('/').split('/')[-1]]
            else:
                try: (resp := self.get(f'https://www.cctalk.com/webapi/content/v1.2/series/all_lesson_list?_timestamp={int(time.time() * 1000)}&seriesId={sid}&showStudyTime=true', **request_overrides)).raise_for_status(); video_ids = [lesson['contentId'] for lesson in resp2json(resp=resp)['data']['items']]
                except Exception: video_ids = [parsed_url.path.strip('/').split('/')[-1]]
            # --iter to parse
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len(video_ids)) as progress:
                for _, video_id in enumerate(video_ids):
                    with suppress(Exception): resp = None; (resp := self.get(f'https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId={video_id}&seriesId=&_timestamp={int(time.time() * 1000)}', **request_overrides)).raise_for_status()
                    if not locals().get('resp') or not hasattr(locals().get('resp'), 'text'): progress.advance(1); continue
                    if not (download_url := safeextractfromdict((raw_data := resp2json(resp=resp)), ['data', 'videoUrl'], '')) or not download_url.startswith('http'): progress.advance(1); continue
                    (video_info_page := copy.deepcopy(video_info)).update(dict(raw_data=raw_data, download_url=download_url))
                    video_title, root_video_title = safeextractfromdict(raw_data, ['data', 'videoName'], None) or null_backup_title, safeextractfromdict(raw_data['data'], ['seriesInfo', 'seriesName'], '')
                    video_title = f"{root_video_title}-EP{len(video_infos)+1}-{video_title}" if root_video_title and len(video_ids) > 1 else f"EP{len(video_infos)+1}-{video_title}" if len(video_ids) > 1 else video_title
                    video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
                    video_info_page.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f"{sid}-{video_id}" if sid else video_id, cover_url=safeextractfromdict(raw_data, ['data', 'coverUrl'], None))); video_infos.append(video_info_page); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"cctalk.com"}
        return BaseVideoClient.belongto(url, valid_domains)