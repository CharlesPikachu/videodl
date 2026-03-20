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
import time
import hashlib
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from .sources import BaseVideoClient
from urllib.parse import urljoin, urlparse, unquote
from typing import Dict, Iterable, List, Optional, Set, Tuple
from .utils import VideoInfo, useparseheaderscookies, requestsproxytodrissionpage


'''Candidate'''
@dataclass(frozen=True)
class Candidate:
    url: str
    source: str
    content_type: Optional[str] = None


'''WebMediaGrabber'''
class WebMediaGrabber(BaseVideoClient):
    source = "WebMediaGrabber"
    LIKELY_MEDIA_CT_PREFIX = ("video/", "audio/")
    LIKELY_PLAYLIST_CT = ("application/vnd.apple.mpegurl", "application/x-mpegurl", "application/mpegurl")
    MEDIA_EXTS = {".mp4", ".m4v", ".mov", ".mkv", ".webm", ".flv", ".f4v", ".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg", ".opus", ".ts", ".m3u8"}
    URL_MAYBE_MEDIA_RE = re.compile(r"""(?P<url>https?://[^\s'"]+?(video|audio|m3u8|mp4|webm|mp3|m4a)[^\s'"]*)""", re.IGNORECASE)
    URL_IN_TEXT_RE = re.compile(r"""(?P<url>https?://[^\s'"]+?(\.mp4|\.m4v|\.mov|\.mkv|\.webm|\.flv|\.mp3|\.m4a|\.aac|\.wav|\.flac|\.ogg|\.opus|\.ts|\.m3u8)(\?[^\s'"]*)?)""", re.IGNORECASE)
    def __init__(self, enable_scroll: bool = True, scroll_rounds: int = 6, scroll_step_px: int = 1400, scroll_pause_ms: int = 600, scroll_settle_ms: int = 1200, request_timeout: int = 12, browser_timeout_sec: int = 25, browser_settle_sec: float = 1.5, browser_headless: bool = True, browser_disable_images: bool = True, browser_load_mode: str = "eager", browser_path: Optional[str] = None, **kwargs):
        super(WebMediaGrabber, self).__init__(**kwargs)
        # scroll settings
        self.enable_scroll = enable_scroll
        self.scroll_rounds = scroll_rounds
        self.scroll_step_px = scroll_step_px
        self.scroll_pause_ms = scroll_pause_ms
        self.scroll_settle_ms = scroll_settle_ms
        # requests settings
        self.request_timeout = request_timeout
        # browser settings
        self.browser_path = browser_path
        self.browser_headless = browser_headless
        self.browser_load_mode = browser_load_mode
        self.browser_settle_sec = browser_settle_sec
        self.browser_timeout_sec = browser_timeout_sec
        self.browser_disable_images = browser_disable_images
        # headers settings
        self.default_parse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36", "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8", "Connection": "keep-alive"}
        self.default_download_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
        self.default_headers = self.default_parse_headers
        # direct media cache
        self._direct_media_cache: Dict[str, Tuple[bool, Optional[str]]] = {}
        # initialization
        self._initsession()
    '''normalizecontenttype'''
    @staticmethod
    def normalizecontenttype(content_type: Optional[str]) -> Optional[str]:
        if not content_type: return None
        return content_type.split(";")[0].strip().lower()
    '''safestripurl'''
    @staticmethod
    def safestripurl(url: str) -> str:
        return (url or "").strip().rstrip(").,;\"'")
    '''guessextfromurl'''
    @staticmethod
    def guessextfromurl(url: str) -> str:
        _, ext = os.path.splitext(urlparse(url).path.lower())
        return ext if ext in WebMediaGrabber.MEDIA_EXTS else ""
    '''lookslikemediaurl'''
    @classmethod
    def lookslikemediaurl(cls, url: Optional[str]) -> bool:
        if not url: return False
        if url.startswith(("blob:", "data:", "javascript:")): return False
        if cls.guessextfromurl(url): return True
        return bool(cls.URL_MAYBE_MEDIA_RE.search(url))
    '''filenamefromurl'''
    @staticmethod
    def filenamefromurl(url: str, fallback_name: str = "media.bin") -> str:
        path = unquote(urlparse(url).path or "")
        name = os.path.basename(path.rstrip("/"))
        return name or fallback_name
    '''hashedfilename'''
    @staticmethod
    def hashedfilename(url: str, fallback_name: str = "media.bin") -> str:
        raw_name = WebMediaGrabber.filenamefromurl(url, fallback_name=fallback_name)
        stem, ext = os.path.splitext(raw_name)
        short_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
        return f"{stem}-{short_hash}{ext}" if stem else f"{short_hash}{ext or '.bin'}"
    '''buildvideoinfos'''
    def buildvideoinfos(self, candidates: Iterable[Candidate], referer: Optional[str] = None) -> List[VideoInfo]:
        video_infos: List[VideoInfo] = []; default_download_headers = dict(self.default_download_headers)
        if referer: default_download_headers.update({'referer': referer})
        for cand in candidates: video_infos.append(VideoInfo(source=self.source, download_url=cand.url, title=(file_name := self.hashedfilename(cand.url)), identifier=file_name, file_path=os.path.join(self.work_dir, self.source, file_name), default_download_headers=default_download_headers))
        return video_infos
    '''dedup'''
    def dedup(self, cands: Iterable[Candidate]) -> List[Candidate]:
        seen: Set[str] = set(); out: List[Candidate] = []
        for cand in cands:
            normalized_url = self.safestripurl(cand.url)
            if not normalized_url or normalized_url in seen: continue
            seen.add(normalized_url); out.append(Candidate(normalized_url, cand.source, cand.content_type))
        return out
    '''splitrequestoverrides'''
    def splitrequestoverrides(self, request_overrides: Optional[dict]) -> Tuple[Dict, Dict, Dict]:
        overrides = dict(request_overrides or {})
        extra_headers = dict(overrides.pop("headers", {}) or {})
        extra_cookies = dict(overrides.pop("cookies", {}) or {})
        overrides.setdefault("timeout", self.request_timeout)
        return extra_headers, extra_cookies, overrides
    '''mergeheaderscookies'''
    def mergeheaderscookies(self, request_overrides: Optional[dict] = None, referer: Optional[str] = None) -> Tuple[Dict, Dict, Dict]:
        extra_headers, extra_cookies, other_kwargs = self.splitrequestoverrides(request_overrides)
        (headers := dict(self.default_headers)).update(extra_headers); cookies = {}
        if referer: headers.setdefault("Referer", referer)
        if isinstance(getattr(self, "default_cookies", None), dict): cookies.update(self.default_cookies)
        cookies.update(extra_cookies)
        return headers, cookies, other_kwargs
    '''isprobablydirectmedia'''
    def isprobablydirectmedia(self, url: str, request_overrides: Optional[dict] = None) -> Tuple[bool, Optional[str]]:
        # naive test
        if not (url := self.safestripurl(url)): return False, None
        if (cached := self._direct_media_cache.get(url)) is not None: return cached
        headers, cookies, other_kwargs = self.mergeheaderscookies(request_overrides=request_overrides); ext = self.guessextfromurl(url)
        if ext and ext != ".m3u8": result = (True, None); self._direct_media_cache[url] = result; return result
        if ext == ".m3u8": result = (True, "application/vnd.apple.mpegurl"); self._direct_media_cache[url] = result; return result
        # head test
        try:
            (resp := self.session.head(url, headers=headers, cookies=cookies, allow_redirects=True, **other_kwargs)).raise_for_status()
            ct = self.normalizecontenttype(resp.headers.get("Content-Type"))
            if ct and (ct.startswith(self.LIKELY_MEDIA_CT_PREFIX) or ct in self.LIKELY_PLAYLIST_CT): result = (True, ct); self._direct_media_cache[url] = result; return result
        except requests.RequestException:
            pass
        # get test
        try:
            (range_headers := dict(headers))["Range"] = "bytes=0-1023"
            (resp := self.get(url, headers=range_headers, cookies=cookies, allow_redirects=True, stream=True, **other_kwargs)).raise_for_status()
            ct = self.normalizecontenttype(resp.headers.get("Content-Type")); resp.close()
            if ct and (ct.startswith(self.LIKELY_MEDIA_CT_PREFIX) or ct in self.LIKELY_PLAYLIST_CT): result = (True, ct); self._direct_media_cache[url] = result; return result
        except requests.RequestException:
            pass
        # return
        result = (False, None); self._direct_media_cache[url] = result
        return result
    '''filterdirectmediacandidates'''
    def filterdirectmediacandidates(self, candidates: Iterable[Candidate], request_overrides: Optional[dict] = None, referer: Optional[str] = None) -> List[Candidate]:
        probe_overrides = dict(request_overrides or {}); probe_headers = dict(probe_overrides.pop("headers", {}) or {}); verified: List[Candidate] = []
        if referer: probe_headers.setdefault("Referer", referer)
        if probe_headers: probe_overrides["headers"] = probe_headers
        for cand in self.dedup(candidates):
            ok, detected_ct = self.isprobablydirectmedia(cand.url, request_overrides=probe_overrides)
            if ok: verified.append(Candidate(url=cand.url, source=cand.source, content_type=cand.content_type or detected_ct))
        return verified
    '''extractmedialinks'''
    def extractmedialinks(self, page_url: str, html_text: Optional[str]) -> List[Candidate]:
        if not html_text: return []
        soup = BeautifulSoup(html_text, "html.parser"); out: List[Candidate] = []
        def add_candidate_func(raw_url: Optional[str], source: str, content_type: Optional[str] = None) -> None:
            if not raw_url or (raw_url := raw_url.strip()).startswith(("blob:", "data:", "javascript:")): return
            if self.lookslikemediaurl((full_url := urljoin(page_url, raw_url))): out.append(Candidate(full_url, source=source, content_type=content_type))
        for tag in soup.find_all(["video", "audio"]):
            add_candidate_func(tag.get("src"), source=f"<{tag.name} src>")
            for attr in ("data-src", "data-url", "data-play", "data-video"): add_candidate_func(tag.get(attr), source=f"<{tag.name} {attr}>")
            for child in tag.find_all("source"): add_candidate_func(child.get("src"), source=f"<source in {tag.name}>"); add_candidate_func(child.get("data-src"), source=f"<source data-src in {tag.name}>")
        for tag in soup.find_all("source"): add_candidate_func(tag.get("src"), source="<source src>"); add_candidate_func(tag.get("data-src"), source="<source data-src>")
        for tag in soup.find_all("a"):
            if not (href := tag.get("href")): continue
            if self.guessextfromurl((full_url := urljoin(page_url, href))): out.append(Candidate(full_url, source="<a href>"))
        common_attrs = ("src", "data-src", "data-url", "data-play", "data-video", "href")
        [add_candidate_func(value, source=f"<{tag.name} {attr}>") for tag in soup.find_all(True) for attr in common_attrs if (value := tag.get(attr))]
        texts = [html_text] + [text for script_tag in soup.find_all("script") if (text := (script_tag.string or script_tag.get_text(strip=False)))]
        for text in texts:
            for match in self.URL_IN_TEXT_RE.finditer(text): out.append(Candidate(match.group("url"), source="regex(ext)"))
            for match in self.URL_MAYBE_MEDIA_RE.finditer(text): out.append(Candidate(match.group("url"), source="regex(maybe)"))
        return self.dedup(out)
    '''fetchhtmlrequests'''
    def fetchhtmlrequests(self, url: str, request_overrides: Optional[dict] = None) -> Optional[str]:
        headers, cookies, other_kwargs = self.mergeheaderscookies(request_overrides=request_overrides)
        try: (resp := self.get(url, headers=headers, cookies=cookies, allow_redirects=True, **other_kwargs)).raise_for_status(); return resp.text
        except requests.RequestException: return None
    '''buildbrowserpage'''
    def buildbrowserpage(self, request_overrides: Optional[dict] = None):
        from DrissionPage import ChromiumOptions, ChromiumPage
        headers, cookies, other_kwargs = self.mergeheaderscookies(request_overrides=request_overrides)
        (co := ChromiumOptions()).headless(self.browser_headless).auto_port(); co.set_load_mode(self.browser_load_mode)
        co.set_timeouts(base=self.browser_timeout_sec, page_load=self.browser_timeout_sec, script=self.browser_timeout_sec)
        co.ignore_certificate_errors(True); co.set_user_agent(headers.get("User-Agent", "") or headers.get("user-agent", ""))
        if (proxy_str := requestsproxytodrissionpage((other_kwargs.get('proxies') or self._autosetproxies()), mode="chromium", strip_auth_for_chromium=False)): co.set_proxy(proxy_str)
        if self.browser_disable_images: co.no_imgs(True)
        if self.browser_path: co.set_browser_path(self.browser_path)
        page = ChromiumPage(co); (extra_headers := dict(headers)).pop("User-Agent", None); extra_headers.pop("user-agent", None)
        if extra_headers: page.set.headers(extra_headers)
        if cookies: page.set.cookies(cookies)
        return page
    '''closebrowserpage'''
    def closebrowserpage(self, page) -> None:
        for method_name in ("quit", "close"):
            try:
                if callable((method := getattr(page, method_name, None))): method(); return
            except Exception: pass
    '''autoscroll'''
    def autoscroll(self, page) -> None:
        from DrissionPage import ChromiumPage; assert isinstance(page, ChromiumPage)
        last_height, pause_sec, settle_sec = -1, max(self.scroll_pause_ms, 0) / 1000.0, max(self.scroll_settle_ms, 0) / 1000.0
        for _ in range(max(1, self.scroll_rounds)):
            try:
                current_height = page.run_js("return document.body ? document.body.scrollHeight : 0;") or 0
                page.run_js(f"window.scrollBy(0, {int(self.scroll_step_px)});"); time.sleep(pause_sec)
                page.run_js("window.scrollTo(0, document.body.scrollHeight);"); time.sleep(pause_sec)
                if current_height == last_height: break
                last_height = current_height
            except Exception:
                break
        time.sleep(settle_sec)
    '''packetcontenttype'''
    def packetcontenttype(self, packet) -> Optional[str]:
        if (response := getattr(packet, "response", None)) is None: return None
        if isinstance((headers := getattr(response, "headers", None)), dict):
            if (ct := self.normalizecontenttype(headers.get("content-type") or headers.get("Content-Type"))): return ct
        for attr in ("mimeType", "mime_type", "content_type", "type"):
            if (ct := self.normalizecontenttype(getattr(response, attr, None))): return ct
        return None
    '''packettocandidate'''
    def packettocandidate(self, packet) -> Optional[Candidate]:
        packet_url: str = getattr(packet, "url", None)
        if not packet_url or packet_url.startswith(("blob:", "data:", "javascript:")): return None
        content_type = self.packetcontenttype(packet); resource_type = (getattr(packet, "resourceType", None) or "").lower(); is_media_like = False
        if content_type: is_media_like = (content_type.startswith(self.LIKELY_MEDIA_CT_PREFIX) or content_type in self.LIKELY_PLAYLIST_CT)
        is_media_like = is_media_like or bool(self.guessextfromurl(packet_url) or resource_type == "media" or self.lookslikemediaurl(packet_url))
        if not is_media_like: return None
        return Candidate(url=packet_url, source=f"drission:network[{resource_type or 'unknown'}]", content_type=content_type)
    '''fetchhtmlandmediadrission'''
    def fetchhtmlandmediadrission(self, url: str, request_overrides: Optional[dict] = None) -> Tuple[Optional[str], List[Candidate]]:
        page = self.buildbrowserpage(request_overrides=request_overrides); html: Optional[str] = None; captured: List[Candidate] = []
        try:
            try: page.listen.start(True, method=True, res_type=True)
            except Exception: pass
            page.get(url); time.sleep(self.browser_settle_sec)
            if self.enable_scroll: self.autoscroll(page)
            time.sleep(self.browser_settle_sec)
            try: page.listen.wait_silent(timeout=self.browser_timeout_sec)
            except Exception: pass
            try: html = page.html
            except Exception: html = None
            try:
                for packet in page.listen.steps(timeout=0.5):
                    packets = packet if isinstance(packet, list) else [packet]
                    for one in packets:
                        if (cand := self.packettocandidate(one)) is not None: captured.append(cand)
            except Exception:
                pass
        finally:
            try: page.listen.stop()
            except Exception: pass
            self.closebrowserpage(page)
        return html, self.dedup(captured)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: Optional[dict] = None):
        request_overrides = request_overrides or {}
        is_direct, _ = self.isprobablydirectmedia(url, request_overrides=request_overrides)
        if is_direct: return self.buildvideoinfos([Candidate(url=url, source="input:direct", content_type=None)], referer=url)
        # 1) Requests Attempt
        html_requests = self.fetchhtmlrequests(url, request_overrides=request_overrides)
        request_candidates = self.extractmedialinks(url, html_requests)
        request_candidates = self.filterdirectmediacandidates(request_candidates, request_overrides=request_overrides, referer=url)
        if request_candidates: return self.buildvideoinfos(request_candidates, referer=url)
        # 2) DrissionPage Fallback
        html_browser, network_candidates = self.fetchhtmlandmediadrission(url, request_overrides=request_overrides)
        merged_candidates: List[Candidate] = []; merged_candidates.extend(network_candidates); merged_candidates.extend(self.extractmedialinks(url, html_browser))
        merged_candidates = self.dedup(merged_candidates); merged_candidates = self.filterdirectmediacandidates(merged_candidates, request_overrides=request_overrides, referer=url)
        if merged_candidates: return self.buildvideoinfos(merged_candidates, referer=url)
        # 3) Failure
        return []