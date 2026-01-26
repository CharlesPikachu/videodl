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
from typing import Mapping, Any
from urllib.parse import urlparse
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import VideoInfo, FileTypeSniffer, RandomIPGenerator, useparseheaderscookies, legalizestring, resp2json, yieldtimerelatedtitle, optionalimport


'''XiazaitoolVideoClient'''
class XiazaitoolVideoClient(BaseVideoClient):
    source = 'XiazaitoolVideoClient'
    def __init__(self, **kwargs):
        if ('enable_parse_curl_cffi' not in kwargs) and optionalimport('curl_cffi'): kwargs['enable_parse_curl_cffi'] = True
        super(XiazaitoolVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "accept": "application/json, text/javascript, */*; q=0.01", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json", "origin": "https://www.xiazaitool.com", "priority": "u=1, i", "referer": "https://www.xiazaitool.com/dy",
            "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty", "sec-fetch-mode": "cors", "sec-fetch-site": "same-origin", "timestamg": str(int(time.time() * 1000)), "x-requested-with": "XMLHttpRequest",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
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
        null_backup_title = yieldtimerelatedtitle(self.source)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        # try parse
        video_infos = []
        try:
            # --post request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            resp = self.post("https://www.xiazaitool.com/video/parseVideoUrl", json=self._confidential({"url": url, "platform": self._detectplatform(url)}), headers=headers, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            # --append all parsed results
            for item in raw_data['data']['voideDeatilVoList']:
                if not isinstance(item, dict) or not item.get('url'): continue
                video_info_page = copy.deepcopy(video_info)
                video_title = legalizestring(item.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                video_info_page.update(dict(download_url=item['url']))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=item['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                if ext in ['xsl', 'm4s']: ext = 'mp4'
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
                ))
                video_infos.append(video_info_page)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos