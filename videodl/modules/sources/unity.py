'''
Function:
    Implementation of UnityVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import copy
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''UnityVideoClient'''
class UnityVideoClient(BaseVideoClient):
    source = 'UnityVideoClient'
    def __init__(self, **kwargs):
        super(UnityVideoClient, self).__init__(**kwargs)
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
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, "lxml")
            script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
            raw_data = json_repair.loads(script_tag.string)
            video_info.update(dict(raw_data=raw_data))
            tutorial: dict = safeextractfromdict(raw_data, ['props', 'pageProps', 'tutorial'], {})
            tutorial_title, sections, videos, uniq = tutorial.get("title", "").strip(), tutorial.get("sections", []), [], set()
            for section in sections:
                if not isinstance(section, dict): continue
                section_title, body = section.get("title", "").strip(), section.get("body", []) or []
                for block in body:
                    if not isinstance(block, dict): continue
                    if block.get("_type") not in ("learn-gcpVideoBlock",): continue
                    ov = block.get("overviewVideo") or {}
                    url = ov.get("url") or ov.get("videoURL")
                    if not url and isinstance(ov, dict):
                        for v in ov.values():
                            if isinstance(v, str) and v.startswith("http"): url = v; break
                    if not url or (not (".mp4" in url or ".m3u8" in url)): continue
                    if section_title and tutorial_title: title = f"{tutorial_title}-ep{len(videos)+1}-{section_title}"
                    else: title = f'ep{len(videos)+1}-' + (section_title or tutorial_title or "Unity Learn Video")
                    if url in uniq: continue
                    uniq.add(url)
                    videos.append({"title": title, "url": url})
            for v in videos:
                video_info_page = copy.deepcopy(video_info)
                video_info_page.update(dict(download_url=v['url']))
                video_title = legalizestring(v['title'], replace_null_string=null_backup_title).removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=v['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info_page['ext']
                video_info_page.update(dict(
                    title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title
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
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"learn.unity.com"}
        return BaseVideoClient.belongto(url, valid_domains)