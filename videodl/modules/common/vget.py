'''
Function:
    Implementation of VgetVideoClient: https://vget.xyz/
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import html
from bs4 import BeautifulSoup
from ..sources import BaseVideoClient
from urllib.parse import parse_qs, urlparse
from ..utils.domains import platformfromurl, obtainhostname, hostmatchessuffix
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, yieldtimerelatedtitle


'''VgetVideoClient'''
class VgetVideoClient(BaseVideoClient):
    source = 'VgetVideoClient'
    def __init__(self, **kwargs):
        super(VgetVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parseresolution'''
    def _parseresolution(self, text: str):
        if not (m := re.search(r'(\d+)\s*x\s*(\d+)', text)): return 0, 0
        w, h = map(int, m.groups())
        return w, h
    '''_parsefilesize'''
    def _parsefilesize(self, text: str):
        if (text := text.strip()) == "-" or not text: return 0
        if not (m := re.match(r'([\d\.]+)\s*([KMG]?B)', text, re.I)): return 0
        value = float(m.group(1)); unit = m.group(2).upper()
        multipliers = {'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'B': 1}
        return int(value * multipliers.get(unit, 1))
    '''_extpriority'''
    def _extpriority(self, ext: str, prefer_ext_order: list | None = None):
        ext = ext.lower()
        if not prefer_ext_order: return 0
        try: return -prefer_ext_order.index(ext)
        except ValueError: return -len(prefer_ext_order)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides, null_backup_title, video_infos, auto_filter_rr_for_youtube = request_overrides or {}, yieldtimerelatedtitle(self.source), [], False
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=False, download_with_ffmpeg=True) if BaseVideoClient.belongto(url, {"ted.com", "xinpianchang.com", "ifeng.com"}) else VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if platformfromurl(url) in {'bilibili'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://www.bilibili.com/'}))
        if platformfromurl(url) in {'weibo'}: video_info.update(dict(default_download_headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', 'Referer': 'https://weibo.com/'}))
        url = (lambda u: f"https://www.youtube.com/watch?v={parse_qs(urlparse(u).query, keep_blank_values=True)['v'][0]}" if u.startswith("https://www.youtube.com/watch?") else u)(url)
        # try parse
        try:
            # --post requests
            (resp := self.post("https://vget.xyz/dl", data={'url': url}, **request_overrides)).raise_for_status(); video_info.update(dict(raw_data=resp.text))
            # --extract video items
            soup, video_items = BeautifulSoup(html.unescape(resp.text), "lxml"), []
            for tr in soup.select("table tr"):
                if len((tds := tr.find_all("td"))) < 4: continue
                format_text, size_text, ext_text, btn = tds[0].get_text(" ", strip=True), tds[1].get_text(" ", strip=True), tds[2].get_text(" ", strip=True), tds[3].select_one(".btn-download[data]")
                if not btn or not btn.get('data'): continue
                w, h = self._parseresolution(format_text)
                video_items.append({"format_desc": format_text, "width": w, "height": h, "area": w * h, "size_bytes": self._parsefilesize(size_text), "ext": ext_text.lower(), "url": btn["data"]})
            # --video title
            video_title = (dd.get_text(strip=True) if (dt:=soup.find("dt", string=lambda s: s and "Title" in s)) and (dd:=dt.find_next_sibling("dd")) else None)
            video_title = legalizestring(video_title or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --sort and select the best
            sorted_video_items = sorted([v for v in video_items if isinstance(v, dict) and (v.get('ext') not in {'mhtml', 'jpg', 'jpeg', 'png', 'gif', 'bmp'})], key=lambda x: (x["area"], self._extpriority(x["ext"], ["m3u8", "webm", "mp4"]), x["size_bytes"]), reverse=True)
            if platformfromurl(url).lower() in {'youtube'} and auto_filter_rr_for_youtube: sorted_video_items = [v for v in sorted_video_items if not hostmatchessuffix(obtainhostname(str(v.get('url'))), ["googlevideo.com"])]
            video_info.update(dict(download_url=(download_url := self._convertspecialdownloadurl(sorted_video_items[0]['url'])[0])))
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            if 'playlist/m3u8' in download_url: guess_video_ext_result['ext'] = 'm3u8'
            # --other infos
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            try: cover_url = [v for v in video_items if isinstance(v, dict) and (v.get('ext') in {'mhtml', 'jpg', 'jpeg', 'png', 'gif', 'bmp'})][0]['url']
            except Exception: cover_url = None
            video_info.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=video_title, cover_url=cover_url)); video_infos.append(video_info)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos