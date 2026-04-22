'''
Function:
    Implementation of PeopleVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import html
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse, urljoin
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''PeopleVideoClient'''
class PeopleVideoClient(BaseVideoClient):
    source = 'PeopleVideoClient'
    def __init__(self, **kwargs):
        super(PeopleVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, base_url: str, html_text: str, request_overrides: dict = None) -> dict:
        soup, request_overrides = BeautifulSoup(html_text, "lxml"), request_overrides or {}
        first_func = lambda *xs: next((html.unescape(x).strip() for x in xs if isinstance(x, str) and x.strip()), "")
        meta_func = lambda css: (lambda node: node.get("content", "") if node else "")(soup.select_one(css))
        attr_func = lambda css, name: (lambda node: node.get(name, "") if node else "")(soup.select_one(css))
        title = first_func(meta_func("meta[property='og:title']"), meta_func("meta[name='twitter:title']"), soup.select_one("h1, h2").get_text(" ", strip=True) if soup.select_one("h1, h2") else "", meta_func("meta[name='description']"), soup.title.get_text(" ", strip=True) if soup.title else "")
        poster = first_func(meta_func("meta[property='og:image']"), meta_func("meta[name='twitter:image']"), attr_func("video", "poster"))
        video = first_func(meta_func("meta[property='og:video']"), meta_func("meta[property='og:video:url']"), attr_func("video source", "src"), attr_func("video", "src"))
        scripts = "\n".join(s.get_text(" ", strip=False) for s in soup.find_all("script"))
        if not video and (m := re.search(r"""src\s*:\s*['"]([^'"]+\.(?:mp4|m3u8)(?:\?[^'"]*)?)['"]""", scripts, re.I)): video = m.group(1)
        if not poster and (m := re.search(r"""poster(?:Url)?\s*:\s*['"]([^'"]+\.(?:jpg|jpeg|png|webp)(?:\?[^'"]*)?)['"]""", scripts, re.I)): poster = m.group(1)
        if not video and (m := re.search(r"""https?://[^\s"'<>]+?\.(?:mp4|m3u8)(?:\?[^\s"'<>]*)?""", html_text, re.I)): video = m.group(0)
        if not poster and (m := re.search(r"""https?://[^\s"'<>]+?\.(?:jpg|jpeg|png|webp)(?:\?[^\s"'<>]*)?""", html_text, re.I)): poster = m.group(0)
        if not video and (m := re.search(r'showPlayer\s*\(\s*\{\s*id\s*:\s*["\']([^"\']+\.xml)["\']', html_text)): video = m.group(1)
        if video and str(video).endswith('xml'): (resp := self.get(f'http://tvplayer.people.com.cn/getXML.php?path={video}&callback=playForMobile&ios=0')).raise_for_status(); video = re.search(r"""\b[\w$.]+\s*\(\s*(['"])((?:https?:)?//[^'"]+|/[^'"]+)\1""", resp.text).group(2)
        return {"title": title, "video_url": urljoin(base_url, video), "cover_url": urljoin(base_url, poster)}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url=url).path.strip('/').split('/')[-1].removesuffix('.html').removesuffix('.htm')
            (resp := self.get(url, **request_overrides)).raise_for_status(); resp.encoding = resp.apparent_encoding
            video_info.update(dict(raw_data=(raw_data := self._extractvideoinfo(f"{urlparse(url).scheme}://{urlparse(url).netloc}", resp.text)))); video_info.update(dict(download_url=raw_data['video_url']))
            video_title = legalizestring(raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=raw_data.get('cover_url')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"people.cn", "people.com.cn"}
        return BaseVideoClient.belongto(url, valid_domains)