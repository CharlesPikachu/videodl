'''
Function:
    Implementation of VideoFKVideoClient: https://www.videofk.com/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import copy
from bs4 import BeautifulSoup
from ..sources import BaseVideoClient
from ..utils.domains import platformfromurl
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, yieldtimerelatedtitle


'''VideoFKVideoClient'''
class VideoFKVideoClient(BaseVideoClient):
    source = 'VideoFKVideoClient'
    def __init__(self, **kwargs):
        if 'enable_parse_curl_cffi' not in kwargs: kwargs['enable_parse_curl_cffi'] = True
        super(VideoFKVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            "cookie": "s_id=WGU4FQv4cCTwpoTiJsvT7NEJickpfHU1aTReuApb; _gid=GA1.2.1043013594.1766816578; fpestid=V073VlcaXHE1sWTkcdQq443oTArRtitOAz9US79UBd1hrlEFs2GB1VXJZS0bRhoN5ShMow; _cc_id=19c1ec36d7eeeb3ca212f1f91099c901; panoramaId_expiry=1767421380656; panoramaId=d09e53fafbb650331acba9f48b8c16d53938fc4f5f628a86250cfa97dc16a655; panoramaIdType=panoIndiv; douyin=eyJpdiI6ImhUaERuQ3AzblVXMDN2Q3RmNTdPQWc9PSIsInZhbHVlIjoiQUlJMG8wNnB4SHhJb2JpYllzblhZZz09IiwibWFjIjoiYjA5MTFkM2VmOTZkNDgwNzA0MTBmOGYyMjM3Nzc1ZWM5ZTlhODkxMmNhYzVlNmY2OTBiZTA0N2E3YTRiMDcxZCJ9; _ga=GA1.1.1950505045.1766816578; _ga_XHH8LXKGMC=GS2.1.s1766828551$o2$g1$t1766828794$j54$l0$h0; XSRF-TOKEN=eyJpdiI6Ik55WFBnZFlXcGUrUEdFS2V5WXVjaFE9PSIsInZhbHVlIjoicVZ5bW5EVllqblhIbmJXVWNWRTFIS2VWOHM1REFaSjJIRzVtY0JoanF0VTNLSmtBcTNaMVhCUXRHMW1EaVBxKyIsIm1hYyI6IjRlN2U4ZWFlMDllMWZhM2E4ZDU0MjBhYWNlNDUyNjFlMTA5MjU4YjVjYjMzYThlZmU5YmJhZmZmNTIwNzIwNDMifQ%3D%3D; youtube=eyJpdiI6IlI4TGFRM080dTJaNnFqMTc3OFE3SlE9PSIsInZhbHVlIjoiMkVnZWhQQzRsZ3ZtTjRcLzhWcEtzalE9PSIsIm1hYyI6IjU0ZmQzMDI4OTJlMjg4ZjE0ZDI1MTlhYjJkNTI4NjVhNmI5MTBmY2Q0NjE0NzFjODEzOGJhYmMxODdlOWQ0NTYifQ%3D%3D",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_download_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        }
        self.default_headers = self.default_parse_headers
    '''_parsewebpage'''
    def _parsewebpage(self, html: str):
        # some necessary functions
        def _parseheight(label: str): return int(m.group(1)) if label and (m := re.search(r'(\d{3,4})\s*p', label.lower())) else None
        def _parsebitratekbps(label: str): return int(m.group(1)) if label and (m := re.search(r'(\d+)\s*kb/s', label.lower())) else None
        def _parsecontainer(label: str): return next((ext for ext in ("mp4", "webm", "m4a", "opus") if ext in (label or "").lower()), None)
        def _parsecodec(label: str): return next((c for c in ("av01", "avc1", "vp9") if c in (label or "").lower()), None)
        def _findsectiondiv(video_info_div: BeautifulSoup, section_name: str): return next((s.find_parent("div", class_="video-files") for s in video_info_div.find_all("strong") if s.get_text(strip=True).upper().rstrip(":") == section_name.upper()), None)
        def _extractformats(section_div: BeautifulSoup, kind: str): return [] if not section_div else [{"kind": kind, "label": (label := a.get_text(" ", strip=True)), "url": a["href"], "height": _parseheight(label), "bitrate_kbps": _parsebitratekbps(label), "container": _parsecontainer(label), "codec": _parsecodec(label)} for a in section_div.find_all("a", href=True)]
        def _sortvideoformats(formats): return sorted(formats, key=lambda f: (f.get("height") or -1, {"mp4": 2, "webm": 1}.get(f.get("container"), 0), {"av01": 3, "vp9": 2, "avc1": 1}.get(f.get("codec"), 0)), reverse=True)
        def _sortaudioformats(formats): return sorted(formats, key=lambda f: (f.get("bitrate_kbps") or -1, {"m4a": 2, "opus": 1}.get(f.get("container"), 0)), reverse=True)
        # iter to parse and select the first
        soup, parsed_results = BeautifulSoup(html, "lxml"), []
        for item in soup.select("div.result-item"):
            video_info = item.select_one("div.video-info")
            if not video_info: continue
            title_el = video_info.select_one("h2.h2")
            title = title_el.get_text(" ", strip=True) if title_el else None
            thumb_a = item.select_one("div.video-photo a[href]")
            thumbnail = thumb_a["href"] if thumb_a else None
            mp4_section, mp3_section = _findsectiondiv(video_info, "MP4"), _findsectiondiv(video_info, "MP3")
            video_formats, audio_formats = _extractformats(mp4_section, kind="video"), _extractformats(mp3_section, kind="audio")
            video_formats_sorted, audio_formats_sorted = _sortvideoformats(video_formats), _sortaudioformats(audio_formats)
            best_height = max([f["height"] for f in video_formats_sorted if f["height"] is not None], default=0)
            parsed_results.append({"title": title, "thumbnail": thumbnail, "best_height": best_height, "video_formats": video_formats_sorted, "audio_formats": audio_formats_sorted})
        # only fetch the first by default
        return parsed_results[0]
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
            # --get request
            headers = copy.deepcopy(self.default_headers)
            RandomIPGenerator().addrandomipv4toheaders(headers)
            try:
                site = platformfromurl(url)
                resp = self.get(f'https://www.videofk.com/{site}-video-download/search?url={url}&select={site}', **request_overrides)
                resp.raise_for_status()
            except:
                resp = self.get(f'https://www.videofk.com/index-video-download/search?url={url}', **request_overrides)
                resp.raise_for_status()
            raw_data: dict = self._parsewebpage(resp.text)
            video_info.update(dict(raw_data=raw_data))
            # --video title
            video_title = legalizestring(raw_data.get('title', null_backup_title) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url for videos and audios
            download_url, audio_download_url = raw_data['video_formats'][0]['url'], 'NULL' if not raw_data['audio_formats'] else raw_data['audio_formats'][0]['url']
            download_url = 'https://downloader.twdown.online/load_url?url=' + download_url[download_url.index('url=')+4:]
            if audio_download_url != 'NULL': audio_download_url = 'https://downloader.twdown.online/load_url?url=' + audio_download_url[audio_download_url.index('url=')+4:]
            download_url = self.get(download_url, **request_overrides).text.strip()
            if audio_download_url != 'NULL': audio_download_url = self.get(audio_download_url, **request_overrides).text.strip()
            # --deal with special download urls
            download_url, is_converter_performed = self._convertspecialdownloadurl(download_url)
            if is_converter_performed: video_info.update(dict(enable_nm3u8dlre=True))
            video_info.update(dict(download_url=download_url))
            if audio_download_url and audio_download_url != 'NULL': video_info.update(dict(audio_download_url=audio_download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            if audio_download_url and audio_download_url != 'NULL':
                guess_audio_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                video_info.update(dict(guess_audio_ext_result=guess_audio_ext_result))
                audio_ext = guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']
                if audio_ext in ['m4s']: audio_ext = 'm4a'
                video_info.update(dict(audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos