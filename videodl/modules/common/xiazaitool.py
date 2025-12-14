'''
Function:
    Implementation of XiazaitoolVideoClient: https://www.xiazaitool.com/dy
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import copy
import hashlib
from datetime import datetime
from typing import Mapping, Any
from urllib.parse import urlparse
from ..sources import BaseVideoClient
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, resp2json


'''XiazaitoolVideoClient'''
class XiazaitoolVideoClient(BaseVideoClient):
    source = 'XiazaitoolVideoClient'
    def __init__(self, **kwargs):
        super(XiazaitoolVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://www.xiazaitool.com",
            "priority": "u=1, i",
            "referer": "https://www.xiazaitool.com/dy",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "timestamg": str(int(time.time() * 1000)),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_confidential'''
    def _confidential(self, params: Mapping[str, Any]) -> str:
        salt = "bf5941f27ee14d9ba9ebb72d89de5dea"
        url, platform = params.get("url"), params.get("platform")
        if not url or not platform: raise ValueError("params must contain non-empty 'url' and 'platform'")
        msg = f"{salt}{url}{platform}".encode("utf-8")
        params['params'] = hashlib.sha256(msg).hexdigest()
        return params
    '''_detectplatform'''
    def _detectplatform(self, url: str) -> str | None:
        host = (urlparse(url).hostname or "").lower()
        if any(x in host for x in ["bilibili.com", "b23.tv", "bili2233.cn"]): return "bilibili"
        if "douyin.com" in host: return "douyin"
        if "kuaishou.com" in host: return "kuaishou"
        if "pipix.com" in host: return "pipix"
        if any(x in host for x in ["xiaohongshu.com", "xhslink.com"]): return "xhs"
        if "tiktok.com" in host: return "tiktok"
        if "ixigua.com" in host: return "xigua"
        if "weishi.qq.com" in host: return "weishi"
        if "weibo.com" in host: return "weibo"
        if any(x in host for x in ["jd.com", "3.cn"]): return "jingdong"
        if any(x in host for x in ["youtube.com", "youtu.be"]): return "youtube"
        if any(x in host for x in ["hao123.com", "haokan.baidu.com"]): return "haokan"
        if any(x in host for x in ["facebook.com", "fb.watch"]): return "facebook"
        if any(x in host for x in ["twitter.com", "x.com"]): return "twitter"
        if "instagram.com" in host: return "instagram"
        if "toutiao.com" in host: return "toutiao"
        return host.split('.')[0]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        # try parse
        video_infos = []
        try:
            # --post request
            payload = self._confidential({"url": url, "platform": self._detectplatform(url)})
            resp = self.post("https://www.xiazaitool.com/video/parseVideoUrl", json=payload, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --append all parsed results
            for item in raw_data['data']['voideDeatilVoList']:
                if not isinstance(item, dict) or not item.get('url'): continue
                video_info_page = copy.deepcopy(video_info)
                dt = datetime.fromtimestamp(time.time())
                date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
                video_title = item.get('title') or f'{self.source}_null_{date_str}'
                video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
                download_url = item['url']
                video_info_page.update(dict(download_url=download_url))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                    guess_video_ext_result=guess_video_ext_result, identifier=download_url,
                ))
                video_infos.append(video_info_page)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos