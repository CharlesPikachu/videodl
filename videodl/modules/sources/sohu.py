'''
Function:
    Implementation of SohuVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, resp2json, touchdir, yieldtimerelatedtitle, VideoInfo


'''SohuVideoClient'''
class SohuVideoClient(BaseVideoClient):
    source = 'SohuVideoClient'
    def __init__(self, **kwargs):
        super(SohuVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parsefromurlwithmytv'''
    @useparseheaderscookies
    def _parsefromurlwithmytv(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            # --obtain vid
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            script_tag, vid = soup.find("script", string=lambda t: t and "var vid" in t), None
            if script_tag:
                m = re.search(r'var\s+vid\s*=\s*"(\d+)"', script_tag.get_text()) or re.search(r"var\s+vid\s*=\s*'(\d+)'", script_tag.get_text())
                vid = m.group(1) if m else None
            if vid is None:
                li = soup.find("li", attrs={"data-vid": True})
                vid = li["data-vid"].strip()
            # --request for the first time to obtain new vid
            resp = self.get(f'http://my.tv.sohu.com/play/videonew.do?vid={vid}&referer=http://my.tv.sohu.com', **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            qualities = ['norVid', 'highVid', 'superVid', 'oriVid'][::-1]
            for quality in qualities:
                vid = raw_data['data'].get(quality, '')
                if vid: break
            # --request again using new vid with higher video quality
            resp = self.get(f'http://my.tv.sohu.com/play/videonew.do?vid={vid}&referer=http://my.tv.sohu.com', **request_overrides)
            resp.raise_for_status()
            raw_data[f'{vid}_videonew.do'] = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            mp4_palyurls, download_urls = raw_data[f'{vid}_videonew.do']["data"]["mp4PlayUrl"], []
            for download_url in mp4_palyurls:
                if not download_url: continue
                if download_url.startswith("//"): download_url = "https:" + download_url
                download_urls.append(download_url)
            # --some download urls need parse twice
            parsed_download_urls = []
            for download_url in download_urls:
                try:
                    resp = self.get(download_url, **request_overrides)
                    resp.raise_for_status()
                    download_url = resp2json(resp=resp)['servers'][0]['url']
                    if download_url: parsed_download_urls.append(download_url)
                except:
                    pass
            if parsed_download_urls: download_urls = parsed_download_urls
            # --construct other video info
            video_title = legalizestring(raw_data["data"].get('tvName', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.mp4'), ext='mp4', vid=vid, identifier=vid,
            ))
            # --if multiple video split
            if len(download_urls) == 1:
                video_info.update(dict(download_url=download_urls[0]))
            else:
                ffmpeg_target_file_path = os.path.join(self.work_dir, self.source, f'{vid}.txt')
                touchdir(os.path.dirname(ffmpeg_target_file_path))
                with open(ffmpeg_target_file_path, "w", encoding="utf-8") as fp:
                    for url in download_urls: fp.write(f"{url}\n")
                video_info.update(dict(download_url=ffmpeg_target_file_path, download_with_ffmpeg=True))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlwithmytv >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''_parsefromurlwithhotvrs'''
    @useparseheaderscookies
    def _parsefromurlwithhotvrs(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        # try parse
        try:
            # --obtain vid
            resp = self.get(url, **request_overrides)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            script_tag, vid = soup.find("script", string=lambda t: t and "var vid" in t), None
            if script_tag:
                m = re.search(r'var\s+vid\s*=\s*"(\d+)"', script_tag.get_text()) or re.search(r"var\s+vid\s*=\s*'(\d+)'", script_tag.get_text())
                vid = m.group(1) if m else None
            if vid is None:
                li = soup.find("li", attrs={"data-vid": True})
                vid = li["data-vid"].strip()
            # --video raw data
            params = {'vid': vid, 'ver': '1', 'ssl': '1', 'uid': '17636986544987061902', 'pflag': 'pch5', 'prod': 'h5n', 'platform_source': 'pc'}
            resp = self.get('https://hot.vrs.sohu.com/vrs_pc_play.action', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data = resp2json(resp=resp)
            if not (raw_data.get('data') and isinstance(raw_data['data'], dict)): return [video_info]
            # --parse
            priority_keys = [
                "relativeId", "norVid", "highVid", "superVid", "oriVid", "h2644kVid", "h265norVid", "h265highVid", "h265superVid", "h265oriVid", "h2654mVid", "h2654kVid", "norVid_ns", "highVid_ns", "superVid_ns", "oriVid_ns", 
                "p1080HdrVid", "p1080Hdr265Vid", "p1080HdrVid_ns", "p1080Hdr265Vid_ns", "tvVer35_vid", "tvVer36_vid", "tvVer34_vid", "tvVer284_vid", "tvVer285_vid", "tvVer260_vid", "tvVer262_vid", "tvVer264_vid", "tvVer266_vid", 
                "tvVer301_vid", "tvVer302_vid", "tvVer303_vid", "tvVer304_vid", "tvVer306_vid", "tvVer307_vid", "tvVer321_vid", "tvVer322_vid", "tvVer323_vid", "tvVer324_vid", "tvVer326_vid", "tvVer327_vid",
            ][::-1]
            for quality in priority_keys:
                vid = raw_data['data'].get(quality, 0)
                if isinstance(vid, str):
                    try: vid = int(vid)
                    except ValueError: vid = 0
                if vid and vid != 0: break
            # --request again using new vid with higher video quality
            params = {'vid': vid, 'ver': '1', 'ssl': '1', 'uid': '17636986544987061902', 'pflag': 'pch5', 'prod': 'h5n', 'platform_source': 'pc'}
            resp = self.get('https://hot.vrs.sohu.com/vrs_pc_play.action', params=params, **request_overrides)
            resp.raise_for_status()
            raw_data[f'{vid}_vrs_pc_play.action'] = resp2json(resp=resp)
            video_info.update(dict(raw_data=raw_data))
            mp4_palyurls, download_urls = raw_data[f'{vid}_vrs_pc_play.action']["data"]["mp4PlayUrl"], []
            for download_url in mp4_palyurls:
                if download_url.startswith("//"): download_url = "https:" + download_url
                download_urls.append(download_url)
            # --some download urls need parse twice
            parsed_download_urls = []
            for download_url in download_urls:
                try:
                    resp = self.get(download_url, **request_overrides)
                    resp.raise_for_status()
                    download_url = resp2json(resp=resp)['servers'][0]['url']
                    if download_url: parsed_download_urls.append(download_url)
                except:
                    pass
            if parsed_download_urls: download_urls = parsed_download_urls
            # --construct other video info
            video_title = legalizestring(raw_data["data"].get('tvName', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.mp4'), ext='mp4', vid=vid, identifier=vid,
            ))
            # --if multiple video split
            if len(download_urls) == 1:
                video_info.update(dict(download_url=download_urls[0]))
            else:
                ffmpeg_target_file_path = os.path.join(self.work_dir, self.source, f'{vid}.txt')
                touchdir(os.path.dirname(ffmpeg_target_file_path))
                with open(ffmpeg_target_file_path, "w", encoding="utf-8") as fp:
                    for url in download_urls: fp.write(f"{url}\n")
                video_info.update(dict(download_url=ffmpeg_target_file_path, download_with_ffmpeg=True))
        except Exception as err:
            err_msg = f'{self.source}._parsefromurlwithhotvrs >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlwithhotvrs, self._parsefromurlwithmytv]:
            video_infos = parser(url, request_overrides)
            if any(((info.get("download_url") or "") not in ("", "NULL")) for info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["tv.sohu.com", "film.sohu.com", "my.tv.sohu.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)