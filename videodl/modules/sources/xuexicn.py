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
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''XuexiCNVideoClient'''
class XuexiCNVideoClient(BaseVideoClient):
    source = 'XuexiCNVideoClient'
    def __init__(self, **kwargs):
        super(XuexiCNVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
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
            vid = parse_qs(urlparse(url).query, keep_blank_values=True)['id'][0]
            (resp := self.get(f"https://boot-source.xuexi.cn/data/app/{vid}.js?callback=callback&_st={int(time.time() * 1000)}", **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(resp.text.removeprefix('callback(').removesuffix(')')))))
            # --iter to parse
            root_video_title = raw_data.get('title', ""); sub_items = raw_data['sub_items']
            for sub_item in sub_items:
                if not isinstance(sub_item, dict): continue
                video_storage_info: list[dict] = sub_item["videos"][0]["video_storage_info"]
                sorted_video_storage_info: list[dict] = sorted(video_storage_info, key=lambda v: (v.get("width", 0) * v.get("height", 0), v.get("bitrate", 0)), reverse=True)
                sorted_video_storage_info: list[dict] = [item for item in sorted_video_storage_info if item.get('normal')]
                (video_info_page := copy.deepcopy(video_info)).update(dict(download_url=(download_url := sorted_video_storage_info[0]['normal'])))
                video_title = (lambda t: f"ep{len(video_infos)+1}-{root_video_title}-{t}" if root_video_title and len(sub_items) > 1 else f"ep{len(video_infos)+1}-{t}" if len(sub_items) > 1 else t)(sub_item.get('title', null_backup_title))
                video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                cover_url = safeextractfromdict(sub_item, ['videos', 0, 'thumbnails', 0, 'data', 0, 'url'], None)
                video_info_page.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f"{vid}-{sub_item['sn']}", cover_url=cover_url)); video_infos.append(video_info_page)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"xuexi.cn"}
        return BaseVideoClient.belongto(url, valid_domains)