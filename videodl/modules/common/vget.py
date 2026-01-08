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
from ..utils import VideoInfo, FileTypeSniffer, useparseheaderscookies, legalizestring, yieldtimerelatedtitle


'''VgetVideoClient'''
class VgetVideoClient(BaseVideoClient):
    source = 'VgetVideoClient'
    def __init__(self, **kwargs):
        super(VgetVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_parseresolution'''
    def _parseresolution(self, text: str):
        m = re.search(r'(\d+)\s*x\s*(\d+)', text)
        if not m: return 0, 0
        w, h = map(int, m.groups())
        return w, h
    '''_parsefilesize'''
    def _parsefilesize(self, text: str):
        text = text.strip()
        if text == "-" or not text: return 0
        m = re.match(r'([\d\.]+)\s*([KMG]?B)', text, re.I)
        if not m: return 0
        value = float(m.group(1))
        unit = m.group(2).upper()
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
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        null_backup_title = yieldtimerelatedtitle(self.source)
        url = (lambda u: f"https://www.youtube.com/watch?v={parse_qs(urlparse(u).query, keep_blank_values=True)['v'][0]}" if u.startswith("https://www.youtube.com/watch?") else u)(url)
        # try parse
        video_infos = []
        try:
            # --post requests
            resp = self.post("https://vget.xyz/dl", data={'url': url}, **request_overrides)
            video_info.update(dict(raw_data=resp.text))
            # --extract video items
            soup, video_items = BeautifulSoup(html.unescape(resp.text), "html.parser"), []
            for tr in soup.select("table tr"):
                tds = tr.find_all("td")
                if len(tds) < 4: continue
                format_text, size_text, ext_text, btn = tds[0].get_text(" ", strip=True), tds[1].get_text(" ", strip=True), tds[2].get_text(" ", strip=True), tds[3].select_one(".btn-download[data]")
                if not btn or not btn.get('data'): continue
                w, h = self._parseresolution(format_text)
                video_items.append({"format_desc": format_text, "width": w, "height": h, "area": w * h, "size_bytes": self._parsefilesize(size_text), "ext": ext_text.lower(), "url": btn["data"]})
            # --video title
            video_title = (dd.get_text(strip=True) if (dt:=soup.find("dt", string=lambda s: s and "Title" in s)) and (dd:=dt.find_next_sibling("dd")) else None)
            video_title = legalizestring(video_title or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            # --sort and select the best
            sorted_video_items = sorted(video_items, key=lambda x: (x["area"], self._extpriority(x["ext"], ["mp4", "webm", "m3u8"]), x["size_bytes"]), reverse=True)
            for item in sorted_video_items:
                download_url, is_converter_performed = self._convertspecialdownloadurl(item['url'])
                if is_converter_performed: video_info.update(dict(enable_nm3u8dlre=True))
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=False if is_converter_performed else True,
                )
                if guess_video_ext_result['ext'] in ['txt', 'NULL']: continue
                break
            video_info.update(dict(download_url=download_url))
            # --other infos
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, enable_nm3u8dlre=True, guess_video_ext_result=guess_video_ext_result, identifier=video_title,
            ))
            video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos