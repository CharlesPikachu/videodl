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
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, taskprogress, FileTypeSniffer, VideoInfo


'''UnityVideoClient'''
class UnityVideoClient(BaseVideoClient):
    source = 'UnityVideoClient'
    def __init__(self, **kwargs):
        super(UnityVideoClient, self).__init__(**kwargs)
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
            (resp := self.get(url, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'
            script_tag = BeautifulSoup(resp.text, "lxml").find("script", id="__NEXT_DATA__", type="application/json")
            video_info.update(dict(raw_data=(raw_data := json_repair.loads(script_tag.string))))
            tutorial: dict = safeextractfromdict(raw_data, ['props', 'pageProps', 'tutorial'], {})
            tutorial_title, extracted_video_items, uniq = str(tutorial.get("title", "")).strip(), [], set()
            for section in (tutorial.get("sections", []) or []):
                if not isinstance(section, dict): continue
                section_title, body = str(section.get("title", "")).strip(), section.get("body", []) or []
                for block in body:
                    if isinstance(block, dict) and block.get("_type") == "learn-gcpVideoBlock" and (overview_video := block.get("overviewVideo") or {}) is not None and (url := overview_video.get("url") or overview_video.get("videoURL") or (next((value for value in overview_video.values() if isinstance(value, str) and value.startswith("http")), "") if isinstance(overview_video, dict) else "")) and any(ext in url for ext in (".mp4", ".m3u8")) and url not in uniq: uniq.add(url); extracted_video_items.append({"title": f"{tutorial_title}-EP{len(extracted_video_items)+1}-{section_title}" if section_title and tutorial_title else f"EP{len(extracted_video_items)+1}-" + (section_title or tutorial_title or "Unity Learn Video"), "url": url})
            cover_url = safeextractfromdict(raw_data, ['props', 'pageProps', 'content', 'coverImageURL'], None)
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len(extracted_video_items)) as progress:
                for extracted_video_item in extracted_video_items:
                    (video_info_page := copy.deepcopy(video_info)).update(dict(download_url=extracted_video_item['url']))
                    video_title = legalizestring(extracted_video_item['title'], replace_null_string=null_backup_title).removesuffix('.')
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=extracted_video_item['url'], headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
                    ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info_page.ext
                    video_info_page.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=cover_url)); video_infos.append(video_info_page); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"learn.unity.com"}
        return BaseVideoClient.belongto(url, valid_domains)