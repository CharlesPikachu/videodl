'''
Function:
    Implementation of WebMediaGrabber
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import os
import re
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from .sources import BaseVideoClient
from urllib.parse import urljoin, urlparse
from typing import Dict, Iterable, List, Optional, Set, Tuple
from .utils import useparseheaderscookies, ensureplaywrightchromium, VideoInfo


'''Candidate'''
@dataclass(frozen=True)
class Candidate:
    url: str
    source: str
    content_type: Optional[str] = None


'''WebMediaGrabber'''
class WebMediaGrabber(BaseVideoClient):
    source = 'WebMediaGrabber'
    LIKELY_MEDIA_CT_PREFIX = ("video/", "audio/")
    LIKELY_PLAYLIST_CT = ("application/vnd.apple.mpegurl", "application/x-mpegurl", "application/mpegurl")
    MEDIA_EXTS = {".mp4", ".m4v", ".mov", ".mkv", ".webm", ".flv", ".f4v", ".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg", ".opus", ".ts", ".m3u8"}
    URL_MAYBE_MEDIA_RE = re.compile(r"""(?P<url>https?://[^\s'"]+?(video|audio|m3u8|mp4|webm|mp3|m4a)[^\s'"]*)""", re.IGNORECASE)
    URL_IN_TEXT_RE = re.compile(r"""(?P<url>https?://[^\s'"]+?(\.mp4|\.m4v|\.mov|\.mkv|\.webm|\.flv|\.mp3|\.m4a|\.aac|\.wav|\.flac|\.ogg|\.opus|\.ts|\.m3u8)(\?[^\s'"]*)?)""", re.IGNORECASE)
    def __init__(self, enable_scroll: bool = True, scroll_rounds: int = 6, scroll_step_px: int = 1400, scroll_pause_ms: int = 600, scroll_settle_ms: int = 1200, **kwargs):
        super(WebMediaGrabber, self).__init__(**kwargs)
        self.enable_scroll = enable_scroll
        self.scroll_rounds = scroll_rounds
        self.scroll_step_px = scroll_step_px
        self.scroll_pause_ms = scroll_pause_ms
        self.scroll_settle_ms = scroll_settle_ms
        self.default_parse_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", "Connection": "keep-alive",
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''guessextfromurl'''
    @staticmethod
    def guessextfromurl(url: str) -> str:
        path = urlparse(url).path
        _, ext = os.path.splitext(path.lower())
        return ext if ext in WebMediaGrabber.MEDIA_EXTS else ""
    '''isprobablydirectmedia'''
    def isprobablydirectmedia(self, url: str, request_overrides: dict = None) -> Tuple[bool, Optional[str]]:
        # init
        request_overrides = request_overrides or {}
        ext = self.guessextfromurl(url)
        if ext and ext != ".m3u8": return True, None
        if ext == ".m3u8": return True, "application/vnd.apple.mpegurl"
        # HEAD
        try:
            resp = self.session.head(url, headers=self.default_parse_headers, cookies=self.default_parse_cookies, allow_redirects=True, **request_overrides)
            ct = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            if ct.startswith(WebMediaGrabber.LIKELY_MEDIA_CT_PREFIX) or ct in WebMediaGrabber.LIKELY_PLAYLIST_CT: return True, ct
        except requests.RequestException:
            pass
        # GET range
        try:
            range_headers = dict(self.default_parse_headers)
            range_headers["Range"] = "bytes=0-1023"
            resp = self.session.get(url, headers=range_headers, cookies=self.default_parse_cookies, allow_redirects=True, stream=True, **request_overrides)
            ct = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            resp.close()
            if ct.startswith(WebMediaGrabber.LIKELY_MEDIA_CT_PREFIX) or ct in WebMediaGrabber.LIKELY_PLAYLIST_CT: return True, ct
        except requests.RequestException:
            pass
        # failure
        return False, None
    '''dedup'''
    def dedup(self, cands: Iterable[Candidate]) -> List[Candidate]:
        seen: Set[str] = set()
        out: List[Candidate] = []
        for c in cands:
            u = (c.url or "").strip().rstrip(").,;\"'")
            if not u or u in seen: continue
            seen.add(u)
            out.append(Candidate(u, c.source, c.content_type))
        return out
    '''extractmedialinks'''
    def extractmedialinks(self, page_url: str, html: str) -> List[Candidate]:
        soup = BeautifulSoup(html or "", "html.parser")
        out: List[Candidate] = []
        # video/audio/src + source/src
        for tag in soup.find_all(["video", "audio"]):
            src = tag.get("src")
            if src: out.append(Candidate(urljoin(page_url, src), source=f"<{tag.name} src>"))
            for s in tag.find_all("source"):
                s_src = s.get("src")
                if s_src: out.append(Candidate(urljoin(page_url, s_src), source=f"<source in {tag.name}>"))
        # standalone source
        for s in soup.find_all("source"):
            s_src = s.get("src")
            if s_src: out.append(Candidate(urljoin(page_url, s_src), source="<source src>"))
        # <a href> with known ext
        for a in soup.find_all("a"):
            href = a.get("href")
            if not href: continue
            u = urljoin(page_url, href)
            if self.guessextfromurl(u): out.append(Candidate(u, source="<a href>"))
        # regex mining from scripts + text
        texts: List[str] = []
        for sc in soup.find_all("script"):
            if sc.string: texts.append(sc.string)
        texts.append(soup.get_text(" ", strip=True))
        for t in texts:
            for m in WebMediaGrabber.URL_IN_TEXT_RE.finditer(t): out.append(Candidate(m.group("url"), source="regex(ext)"))
            for m in WebMediaGrabber.URL_MAYBE_MEDIA_RE.finditer(t): out.append(Candidate(m.group("url"), source="regex(maybe)"))
        # return
        return out
    '''fetchhtmlrequests'''
    def fetchhtmlrequests(self, url: str, request_overrides: dict = None) -> Optional[str]:
        request_overrides = request_overrides or {}
        try:
            resp = self.session.get(url, headers=self.default_parse_headers, cookies=self.default_parse_cookies, allow_redirects=True, **request_overrides)
            resp.raise_for_status()
            return resp.text
        except: return None
    '''autoscroll'''
    def autoscroll(self, page) -> None:
        from playwright.sync_api import Page
        assert isinstance(page, Page)
        try: last_h = page.evaluate("() => document.body.scrollHeight")
        except Exception: last_h = None
        for _ in range(max(1, self.scroll_rounds)):
            try:
                page.evaluate(f"() => window.scrollBy(0, {int(self.scroll_step_px)})")
                page.wait_for_timeout(int(self.scroll_pause_ms))
                page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(int(self.scroll_pause_ms))
                new_h = page.evaluate("() => document.body.scrollHeight")
                if last_h is not None and new_h == last_h: break
                last_h = new_h
            except Exception: break
        try: page.wait_for_timeout(int(self.scroll_settle_ms))
        except Exception: pass
    '''synccookiestorequests'''
    def synccookiestorequests(self, pw_cookies: List[Dict]) -> None:
        for c in pw_cookies:
            name, value, domain, path = c.get("name"), c.get("value"), c.get("domain"), c.get("path", "/")
            if not name or value is None: continue
            self.session.cookies.set(name, value, domain=domain, path=path)
    '''fetchhtmlplaywright'''
    def fetchhtmlplaywright(self, url: str, wait_until: str = "domcontentloaded", timeout_ms: int = 25000, settle_ms: int = 1200, launch_kwargs: dict = None) -> Optional[str]:
        ensureplaywrightchromium()
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            launch_kwargs = launch_kwargs or {"headless": True}
            browser = p.chromium.launch(**launch_kwargs)
            context = browser.new_context(user_agent=self.default_parse_headers.get("User-Agent"), extra_http_headers={k: v for k, v in self.default_parse_headers.items() if k.lower() != "connection"}, ignore_https_errors=True)
            page = context.new_page()
            page.goto(url, wait_until=wait_until, timeout=timeout_ms)
            try: page.wait_for_load_state("networkidle", timeout=timeout_ms)
            except Exception: pass
            if self.enable_scroll: self.autoscroll(page)
            page.wait_for_timeout(settle_ms)
            try: html = page.content()
            except Exception: html = None
            try: self.synccookiestorequests(context.cookies())
            except Exception: pass
            context.close()
            browser.close()
        return html
    '''fetchhtmlandmediaplaywright'''
    def fetchhtmlandmediaplaywright(self, url: str, wait_until: str = "domcontentloaded", timeout_ms: int = 30000, settle_ms: int = 1500, launch_kwargs: dict = None) -> Tuple[Optional[str], List[Candidate]]:
        ensureplaywrightchromium()
        from playwright.sync_api import Response
        from playwright.sync_api import sync_playwright
        captured: List[Candidate] = []
        def _normct(ct: Optional[str]) -> str: return "" if not ct else ct.split(";")[0].strip().lower()
        def _ismediact(ct: str) -> bool: return ct.startswith(WebMediaGrabber.LIKELY_MEDIA_CT_PREFIX) or (ct in WebMediaGrabber.LIKELY_PLAYLIST_CT)
        with sync_playwright() as p:
            launch_kwargs = launch_kwargs or {"headless": True}
            browser = p.chromium.launch(**launch_kwargs)
            context = browser.new_context(user_agent=self.default_parse_headers.get("User-Agent"), extra_http_headers={k: v for k, v in self.default_parse_headers.items() if k.lower() != "connection"}, ignore_https_errors=True)
            page = context.new_page()
            def _onresponse(resp: Response):
                try:
                    u = resp.url
                    if u.startswith("blob:"): return
                    ct = _normct(resp.headers.get("content-type"))
                    if _ismediact(ct) or (self.guessextfromurl(u) in WebMediaGrabber.MEDIA_EXTS): captured.append(Candidate(u, source="playwright:response", content_type=ct or None))
                except Exception:
                    pass
            page.on("response", _onresponse)
            try:
                page.goto(url, wait_until=wait_until, timeout=timeout_ms)
                try: page.wait_for_load_state("networkidle", timeout=timeout_ms)
                except Exception: pass
                if self.enable_scroll: self.autoscroll(page)
                page.wait_for_timeout(settle_ms)
                html = page.content()
            except:
                html: Optional[str] = None
            finally:
                try: self.synccookiestorequests(context.cookies())
                except Exception: pass
                context.close()
                browser.close()
        return html, self.dedup(captured)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # init
        request_overrides = request_overrides or {}
        # direct media link
        is_direct = self.isprobablydirectmedia(url, request_overrides=request_overrides)[0]
        if is_direct: return [VideoInfo(
            source=self.source, download_url=url, title=urlparse(url).path.strip('/').split('/')[-1], identifier=urlparse(url).path.strip('/').split('/')[-1],
            file_path=os.path.join(self.work_dir, self.source, urlparse(url).path.strip('/').split('/')[-1]),
        )]
        self.default_download_headers.update({'Referer': url})
        # non-direct media link, extract from requests html
        html_r = self.fetchhtmlrequests(url, request_overrides)
        cands_r = self.dedup(self.extractmedialinks(url, html_r)) if html_r else []
        cands_r = [cand_r for cand_r in cands_r if self.isprobablydirectmedia(cand_r.url, request_overrides=request_overrides)[0]]
        video_infos = [VideoInfo(
            source=self.source, download_url=cand_r.url, title=urlparse(cand_r.url).path.strip('/').split('/')[-1], identifier=urlparse(cand_r.url).path.strip('/').split('/')[-1],
            file_path=os.path.join(self.work_dir, self.source, urlparse(cand_r.url).path.strip('/').split('/')[-1]),
        ) for cand_r in cands_r]
        if cands_r: return video_infos
        # non-direct media link, extract from Playwright html
        html_pw = self.fetchhtmlplaywright(url)
        cands_pw = self.dedup(self.extractmedialinks(url, html_pw)) if html_pw else []
        cands_pw = [cand_pw for cand_pw in cands_pw if self.isprobablydirectmedia(cand_pw.url, request_overrides=request_overrides)[0]]
        video_infos = [VideoInfo(
            source=self.source, download_url=cand_pw.url, title=urlparse(cand_pw.url).path.strip('/').split('/')[-1], identifier=urlparse(cand_pw.url).path.strip('/').split('/')[-1],
            file_path=os.path.join(self.work_dir, self.source, urlparse(cand_pw.url).path.strip('/').split('/')[-1]),
        ) for cand_pw in cands_pw]
        if cands_pw: return video_infos
        # non-direct media link, extract from Playwright html with network cands
        html_pw, cands_net = self.fetchhtmlandmediaplaywright(url)
        if html_pw: cands_net.extend(self.extractmedialinks(url, html_pw))
        cands_net = self.dedup(cands_net)
        cands_net = [cand_net for cand_net in cands_net if self.isprobablydirectmedia(cand_net.url, request_overrides=request_overrides)[0]]
        video_infos = [VideoInfo(
            source=self.source, download_url=cand_net.url, title=urlparse(cand_net.url).path.strip('/').split('/')[-1], identifier=urlparse(cand_net.url).path.strip('/').split('/')[-1],
            file_path=os.path.join(self.work_dir, self.source, urlparse(cand_net.url).path.strip('/').split('/')[-1]),
        ) for cand_net in cands_pw]
        if cands_net: return video_infos
        # failure
        return []