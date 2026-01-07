'''
Function:
    Implementation of WeishiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''WeishiVideoClient'''
class WeishiVideoClient(BaseVideoClient):
    source = 'WeishiVideoClient'
    def __init__(self, **kwargs):
        super(WeishiVideoClient, self).__init__(**kwargs)
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
        try:
            parsed_url = urlparse(url)
            if 'id' in parse_qs(parsed_url.query, keep_blank_values=True):
                vid = parse_qs(parsed_url.query, keep_blank_values=True)['id'][0]
            else:
                vid = parsed_url.path.strip('/').split('/')[-1]
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            script_tag = soup.find("script", string=re.compile(r"window\.Vise\.initState"))
            script_text = script_tag.string or script_tag.get_text()
            m = re.search(r"window\.Vise\.initState\s*=\s*({.*?});", script_text, re.S)
            raw_data = json_repair.loads(m.group(1))
            video_info.update(dict(raw_data=raw_data))
            video_spec_urls: dict = raw_data["feedsList"][0]["videoSpecUrls"]
            spec_list: list[dict] = list(video_spec_urls.values())
            spec_list = [s for s in spec_list if s.get('url')]
            def _qualityscore(spec: dict):
                vq, w, h = spec.get("videoQuality") or 0, spec.get("width") or 0, spec.get("height") or 0
                fps, size = spec.get("fps") or 0, int(spec.get("size") or 0)
                return (vq, w * h, fps, size)
            spec_list_sorted: list[dict] = sorted(spec_list, key=_qualityscore, reverse=True)
            spec_list_sorted: list[dict] = [item for item in spec_list_sorted if item.get('url')]
            if len(spec_list_sorted) > 0: download_url = spec_list_sorted[0]['url']
            else: download_url = raw_data["feedsList"][0]['videoUrl']
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data["feedsList"][0].get('feedDesc', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid,
            ))
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["isee.weishi.qq.com", "h5.weishi.qq.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)