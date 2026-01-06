'''
Function:
    Implementation of Open163VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, resp2json, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''Open163VideoClient'''
class Open163VideoClient(BaseVideoClient):
    source = 'Open163VideoClient'
    def __init__(self, **kwargs):
        super(Open163VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "host": "c.open.163.com",
            "origin": "https://open.163.com",
            "referer": "https://open.163.com/",
            "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
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
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        video_infos = []
        try:
            parsed_url = urlparse(url)
            pid = parse_qs(parsed_url.query, keep_blank_values=True)['pid'][0]
            resp = self.get(f"https://c.open.163.com/open/mob/movie/list.do?plid={pid}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            root_video_title = raw_data['data'].get('title', "")
            for idx, item in enumerate(raw_data['data']['videoList']):
                if not isinstance(item, dict): continue
                video_info_page = copy.deepcopy(video_info)
                quality_rank, streams = {"Sd": 1, "Hd": 2, "Shd": 3}, []
                for proto in ("mp4", "m3u8"):
                    for level in ("Sd", "Hd", "Shd"):
                        url  = item.get(f"{proto}{level}UrlOrign") or item.get(f"{proto}{level}Url") or ""
                        size = item.get(f"{proto}{level}SizeOrign") or item.get(f"{proto}{level}Size") or 0
                        if not url or size == 0: continue
                        streams.append({"proto": proto, "level": level, "url": url, "size": size, "rank": quality_rank[level]})
                streams_sorted = sorted(streams, key=lambda s: (s["rank"], s["size"]), reverse=True)
                download_url = streams_sorted[0]['url']
                video_info_page.update(dict(download_url=download_url))
                video_title = item.get('title', null_backup_title)
                if root_video_title and len(raw_data['data']['videoList']) > 1: video_title = f"{root_video_title}-ep{idx+1}-{video_title}"
                elif len(raw_data['data']['videoList']) > 1: video_title = f"ep{idx+1}-{video_title}"
                video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f"{item.get('mid')}-{item.get('plid')}",
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
            valid_domains = ["open.163.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)