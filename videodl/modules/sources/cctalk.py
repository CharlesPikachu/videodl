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
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, FileTypeSniffer, VideoInfo


'''CCtalkVideoClient'''
class CCtalkVideoClient(BaseVideoClient):
    source = 'CCtalkVideoClient'
    def __init__(self, **kwargs):
        super(CCtalkVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "harmony-os": "pcweb",
            "host": "www.cctalk.com",
            "hujiang-app-key": "pcweb",
            "referer": "https://www.cctalk.com/v/17604950351552?sid=1760494906733025",
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        # try parse
        video_infos = []
        try:
            # --fetech video ids
            parsed_url = urlparse(url)
            try: sid = parse_qs(parsed_url.query, keep_blank_values=True)['sid'][0]
            except: sid = None
            if not sid:
                video_ids = [parsed_url.path.strip('/').split('/')[-1]]
            else:
                try:
                    resp = self.get(f'https://www.cctalk.com/webapi/content/v1.2/series/all_lesson_list?_timestamp={int(time.time() * 1000)}&seriesId={sid}&showStudyTime=true', **request_overrides)
                    resp.raise_for_status()
                    all_lesson_list = resp2json(resp=resp)['data']['items']
                    video_ids = [lesson['contentId'] for lesson in all_lesson_list]
                except:
                    video_ids = [parsed_url.path.strip('/').split('/')[-1]]
            # --iter to parse
            for video_id in video_ids:
                video_info_page = copy.deepcopy(video_info)
                try:
                    resp = self.get(f'https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId={video_id}&seriesId=&_timestamp={int(time.time() * 1000)}', **request_overrides)
                    resp.raise_for_status()
                    raw_data = resp2json(resp=resp)
                    download_url = raw_data['data']['videoUrl']
                except:
                    continue
                video_info_page.update(dict(raw_data=raw_data))
                video_info_page.update(dict(download_url=download_url))
                dt = datetime.fromtimestamp(time.time())
                date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
                video_title = raw_data['data'].get('videoName', f'{self.source}_null_{date_str}')
                root_video_title = raw_data['data'].get('seriesInfo', {}).get('seriesName', '')
                if root_video_title and len(video_ids) > 1: video_title = f"{root_video_title}_{video_title}"
                video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                    guess_video_ext_result=guess_video_ext_result, identifier=f"{sid}_{video_id}" if sid else video_id,
                ))
                video_infos.append(video_info_page)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.cctalk.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)