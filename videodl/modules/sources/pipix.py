'''
Function:
    Implementation of PipixVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from urllib.parse import unquote
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, resp2json, FileTypeSniffer, VideoInfo


'''PipixVideoClient'''
class PipixVideoClient(BaseVideoClient):
    source = 'PipixVideoClient'
    def __init__(self, **kwargs):
        super(PipixVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            (resp := self.get(url, allow_redirects=True, **request_overrides)).raise_for_status()
            if re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', resp.text):
                raw_data = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', resp.text).group(1)
                video_info.update(dict(raw_data=(raw_data := json_repair.loads(unquote(raw_data)))))
                video_info.update(dict(download_url=(download_url := safeextractfromdict(raw_data, ['ppxItemDetail', 'item', 'video', 'video_download', 'url_list', 0, 'url'], ''))))
                video_title = legalizestring(safeextractfromdict(raw_data, ['ppxItemDetail', 'item', 'video', 'title'], None) or safeextractfromdict(raw_data, ['ppxItemDetail', 'item', 'share', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
                cover_url = safeextractfromdict(raw_data, ['ppxItemDetail', 'item', 'cover', 'url_list', 0, 'url'], None)
                video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=safeextractfromdict(raw_data, ['ppxItemDetail', 'item', 'item_id'], None), cover_url=cover_url))
            else:
                (video_id := re.findall(r'item/(\d+)', resp.url)[0])
                (resp := self.get(f"https://api.pipix.com/bds/cell/cell_comment/?offset=0&cell_type=1&api_version=1&cell_id={video_id}&ac=wifi&channel=huawei_1319_64&aid=1319&app_name=super", **request_overrides)).raise_for_status()
                video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
                data: dict = raw_data["data"]["cell_comments"][0]["comment_info"]["item"]; author_id, download_url = data["author"]["id"], ""
                download_url = next((u for c in data.get("comments", []) if safeextractfromdict(c, ['item', 'author', 'id'], None) == author_id and (u := (((safeextractfromdict(c, ['item', 'video', 'video_high', 'url_list'], None) or [{}])[0]).get("url")))), None)
                video_info.update(dict(download_url=(download_url := data["video"]["video_high"]["url_list"][0]["url"] if not download_url else download_url)))
                video_title = legalizestring(data.get('content', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
                cover_url = safeextractfromdict(raw_data, ['data', 'cell_comments', 0, 'comment_info', 'item', 'cover', 'url_list', 0, 'url'], None)
                video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_id, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"pipix.com"}
        return BaseVideoClient.belongto(url, valid_domains)