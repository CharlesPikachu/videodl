'''
Function:
    Implementation of KuaishouVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import json_repair
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''KuaishouVideoClient'''
class KuaishouVideoClient(BaseVideoClient):
    source = 'KuaishouVideoClient'
    def __init__(self, **kwargs):
        super(KuaishouVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Referer': 'https://v.kuaishou.com/',
        }
        self.default_download_headers = {}
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
            vid = urlparse(url).path.strip('/').split('/')[-1]
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'lxml')
            pattern = r'window\.__APOLLO_STATE__\s*=\s*(\{.*?\});'
            raw_data = json_repair.loads(re.search(pattern, str(soup), re.S).group(1))
            video_info.update(dict(raw_data=raw_data))
            client: dict = raw_data["defaultClient"]
            photo_key = ""
            for k, v in client.items():
                if isinstance(v, dict) and v.get("__typename") == "VisionVideoDetailPhoto": photo_key = k; break
            photo: dict = client[photo_key]
            candidates = []
            if photo.get("photoH265Url"): candidates.append({"codec": "hevc_single", "maxBitrate": 1, "resolution": 1, "url": photo["photoH265Url"], "qualityLabel": "single_hevc"})
            if photo.get("photoUrl"): candidates.append({"codec": "h264_single", "maxBitrate": 1, "resolution": 1, "url": photo["photoUrl"], "qualityLabel": "single_h264"})
            vr = photo.get("videoResource")
            if isinstance(vr, dict):
                vr_json: dict = vr.get("json", {})
                for codec_name in ["hevc", "h264"]:
                    codec = vr_json.get(codec_name)
                    if not codec or not isinstance(codec, dict): continue
                    for aset in codec.get("adaptationSet", []):
                        for rep in aset.get("representation", []):
                            url = rep.get("url")
                            if not url: continue
                            width, height, max_br = rep.get("width", 0), rep.get("height", 0), rep.get("maxBitrate", 0)
                            candidates.append({"codec": codec_name, "maxBitrate": max_br, "resolution": width * height, "url": url, "qualityLabel": rep.get("qualityLabel")})
            codec_priority = {"hevc": 2, "hevc_single": 2, "h264": 1, "h264_single": 1}
            def _sortkey(c):
                return (codec_priority.get(c["codec"], 0), c["maxBitrate"], c["resolution"])
            candidates = [c for c in candidates if c.get('url')]
            candidates.sort(key=_sortkey, reverse=True)
            download_url = [c["url"] for c in candidates][0]
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(photo.get('caption', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid
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
            valid_domains = ["www.kuaishou.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)