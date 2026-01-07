'''
Function:
    Implementation of XuexiCNVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import copy
import json_repair
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''XuexiCNVideoClient'''
class XuexiCNVideoClient(BaseVideoClient):
    source = 'XuexiCNVideoClient'
    def __init__(self, **kwargs):
        super(XuexiCNVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
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
            vid = parse_qs(parsed_url.query, keep_blank_values=True)['id'][0]
            resp = self.get(f"https://boot-source.xuexi.cn/data/app/{vid}.js?callback=callback&_st={int(time.time() * 1000)}", **request_overrides)
            resp.raise_for_status()
            raw_data = resp.text.removeprefix('callback(').removesuffix(')')
            raw_data = json_repair.loads(raw_data)
            video_info.update(dict(raw_data=raw_data))
            root_video_title = raw_data.get('title', "")
            # --iter to parse
            sub_items = raw_data['sub_items']
            for sub_item in sub_items:
                if not isinstance(sub_item, dict): continue
                video_info_page = copy.deepcopy(video_info)
                video_storage_info: list[dict] = sub_item["videos"][0]["video_storage_info"]
                sorted_video_storage_info = sorted(video_storage_info, key=lambda v: (v.get("width", 0) * v.get("height", 0), v.get("bitrate", 0)), reverse=True)
                download_url = sorted_video_storage_info[0]['normal']
                video_info_page.update(dict(download_url=download_url))
                video_title = sub_item.get('title', null_backup_title)
                if root_video_title and len(sub_items) > 1: video_title = f"ep{len(video_infos)+1}-{root_video_title}-{video_title}"
                elif len(sub_items) > 1: video_title = f"ep{len(video_infos)+1}-{video_title}"
                video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f"{vid}-{sub_item['sn']}",
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
            valid_domains = ["www.xuexi.cn"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)