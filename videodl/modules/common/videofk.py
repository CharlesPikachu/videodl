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
from ..utils.domains import platformfromurl, obtainhostname, hostmatchessuffix
from ..utils import RandomIPGenerator, VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, yieldtimerelatedtitle, safeextractfromdict


'''VideoFKVideoClient'''
class VideoFKVideoClient(BaseVideoClient):
    source = 'VideoFKVideoClient'
    def __init__(self, **kwargs):
        super(VideoFKVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {"cookie": "s_id=WGU4FQv4cCTwpoTiJsvT7NEJickpfHU1aTReuApb; _gid=GA1.2.1043013594.1766816578; fpestid=V073VlcaXHE1sWTkcdQq443oTArRtitOAz9US79UBd1hrlEFs2GB1VXJZS0bRhoN5ShMow; _cc_id=19c1ec36d7eeeb3ca212f1f91099c901; panoramaId_expiry=1767421380656; panoramaId=d09e53fafbb650331acba9f48b8c16d53938fc4f5f628a86250cfa97dc16a655; panoramaIdType=panoIndiv; douyin=eyJpdiI6ImhUaERuQ3AzblVXMDN2Q3RmNTdPQWc9PSIsInZhbHVlIjoiQUlJMG8wNnB4SHhJb2JpYllzblhZZz09IiwibWFjIjoiYjA5MTFkM2VmOTZkNDgwNzA0MTBmOGYyMjM3Nzc1ZWM5ZTlhODkxMmNhYzVlNmY2OTBiZTA0N2E3YTRiMDcxZCJ9; _ga=GA1.1.1950505045.1766816578; _ga_XHH8LXKGMC=GS2.1.s1766828551$o2$g1$t1766828794$j54$l0$h0; XSRF-TOKEN=eyJpdiI6Ik55WFBnZFlXcGUrUEdFS2V5WXVjaFE9PSIsInZhbHVlIjoicVZ5bW5EVllqblhIbmJXVWNWRTFIS2VWOHM1REFaSjJIRzVtY0JoanF0VTNLSmtBcTNaMVhCUXRHMW1EaVBxKyIsIm1hYyI6IjRlN2U4ZWFlMDllMWZhM2E4ZDU0MjBhYWNlNDUyNjFlMTA5MjU4YjVjYjMzYThlZmU5YmJhZmZmNTIwNzIwNDMifQ%3D%3D; youtube=eyJpdiI6IlI4TGFRM080dTJaNnFqMTc3OFE3SlE9PSIsInZhbHVlIjoiMkVnZWhQQzRsZ3ZtTjRcLzhWcEtzalE9PSIsIm1hYyI6IjU0ZmQzMDI4OTJlMjg4ZjE0ZDI1MTlhYjJkNTI4NjVhNmI5MTBmY2Q0NjE0NzFjODEzOGJhYmMxODdlOWQ0NTYifQ%3D%3D", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
        self.default_download_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
    '''_parsewebpage'''
    def _parsewebpage(self, html: str) -> dict:
        # some necessary functions
        parseheight_func = lambda label: (int(m.group(1)) if label and (m := re.search(r'(\d{3,4})\s*p', str(label).lower())) else None)
        parsebitratekbps_func = lambda label: (int(m.group(1)) if label and (m := re.search(r'(\d+)\s*kb/s', str(label).lower())) else None)
        parsecontainer_func = lambda label: next((ext for ext in ("mp4", "webm", "m4a", "opus") if ext in (label or "").lower()), None)
        parsecodec_func = lambda label: next((c for c in ("av01", "avc1", "vp9") if c in (label or "").lower()), None)
        findsectiondiv_func = lambda video_info_div, section_name: next((s.find_parent("div", class_="video-files") for s in video_info_div.find_all("strong") if s.get_text(strip=True).upper().rstrip(":") == section_name.upper()), None)
        extractformats_func = lambda section_div, kind: ([] if not section_div else [{"kind": kind, "label": (label := a.get_text(" ", strip=True)), "url": a["href"], "height": parseheight_func(label), "bitrate_kbps": parsebitratekbps_func(label), "container": parsecontainer_func(label), "codec": parsecodec_func(label)} for a in section_div.find_all("a", href=True)])
        sortvideoformats_func = lambda formats: sorted(formats, key=lambda f: ((f.get("height") or -1), {"mp4": 2, "webm": 1}.get(f.get("container"), 0), {"av01": 3, "vp9": 2, "avc1": 1}.get(f.get("codec"), 0)), reverse=True)
        sortaudioformats_func = lambda formats: sorted(formats, key=lambda f: ((f.get("bitrate_kbps") or -1), {"m4a": 2, "opus": 1}.get(f.get("container"), 0)), reverse=True)
        # iter to parse and select the first
        soup, parsed_results = BeautifulSoup(html, "lxml"), []
        for item in soup.select("div.result-item"):
            if not (video_info := item.select_one("div.video-info")): continue
            title_el = video_info.select_one("h2.h2"); title = title_el.get_text(" ", strip=True) if title_el else None
            thumb_a = item.select_one("div.video-photo a[href]"); thumbnail = thumb_a["href"] if thumb_a else None
            mp4_section, mp3_section = findsectiondiv_func(video_info, "MP4"), findsectiondiv_func(video_info, "MP3")
            video_formats, audio_formats = extractformats_func(mp4_section, kind="video"), extractformats_func(mp3_section, kind="audio")
            video_formats_sorted, audio_formats_sorted = sortvideoformats_func(video_formats), sortaudioformats_func(audio_formats)
            best_height = max([f["height"] for f in video_formats_sorted if f["height"] is not None], default=0)
            parsed_results.append({"title": title, "thumbnail": thumbnail, "best_height": best_height, "video_formats": video_formats_sorted, "audio_formats": audio_formats_sorted})
        # only fetch the first by default
        return parsed_results[0]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        request_overrides, null_backup_title, video_infos, auto_filter_rr_for_youtube = request_overrides or {}, yieldtimerelatedtitle(self.source), [], False
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://weibo.com/'}))
        # try parse
        try:
            # --get request
            headers = copy.deepcopy(self.default_headers); RandomIPGenerator().addrandomipv4toheaders(headers)
            try: site = platformfromurl(url); (resp := self.get(f'https://www.videofk.com/{site}-video-download/search?url={url}&select={site}', **request_overrides)).raise_for_status()
            except: (resp := self.get(f'https://www.videofk.com/index-video-download/search?url={url}', **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := self._parsewebpage(resp.text))))
            # --video title
            video_title = legalizestring(raw_data.get('title', null_backup_title) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --download url for videos and audios
            if platformfromurl(url).lower() in {'youtube'} and auto_filter_rr_for_youtube: download_url = next((u for fmt in raw_data["video_formats"] if not hostmatchessuffix(obtainhostname(str(u := self.get("https://downloader.twdown.online/load_url?url=" + (s := fmt["url"])[s.index("url=")+4:], **request_overrides).text.strip()) if "url=" in fmt["url"] else (u := fmt["url"])), ["googlevideo.com"])), None)
            else: download_url: str = raw_data['video_formats'][0]['url']; download_url = self.get('https://downloader.twdown.online/load_url?url=' + download_url[download_url.index('url=')+4:], **request_overrides).text.strip() if 'url=' in download_url else download_url
            audio_download_url = 'NULL' if not raw_data['audio_formats'] else safeextractfromdict(raw_data, ['audio_formats', 0, 'url'], None)
            if audio_download_url and (audio_download_url not in {'NULL', 'None'}): audio_download_url = self.get('https://downloader.twdown.online/load_url?url=' + audio_download_url[audio_download_url.index('url=')+4:], **request_overrides).text.strip()
            # --deal with special download urls
            video_info.update(dict(download_url=(download_url := self._convertspecialdownloadurl(download_url)[0])))
            if audio_download_url and (audio_download_url not in {'NULL', 'None'}): video_info.update(dict(audio_download_url=audio_download_url))
            # --other infos
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=raw_data.get('thumbnail')))
            if audio_download_url and (audio_download_url not in {'NULL', 'None'}):
                video_info.update(dict(guess_audio_ext_result=(guess_audio_ext_result := FileTypeSniffer.getfileextensionfromurl(url=audio_download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies))))
                if (audio_ext := guess_audio_ext_result['ext'] if guess_audio_ext_result['ext'] and guess_audio_ext_result['ext'] != 'NULL' else video_info['audio_ext']) in {'m4s', 'mp4'}: audio_ext = 'm4a'
                video_info.update(dict(audio_ext=audio_ext, audio_file_path=os.path.join(self.work_dir, self.source, f'{video_title}.audio.{audio_ext}')))
            video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos