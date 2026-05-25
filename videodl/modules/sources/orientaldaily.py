'''
Function:
    Implementation of OrientalDailyVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import html
import json
from .base import BaseVideoClient
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse, urljoin
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, VideoInfo, FileTypeSniffer


'''OrientalDailyVideoClient'''
class OrientalDailyVideoClient(BaseVideoClient):
    source = 'OrientalDailyVideoClient'
    VIDEO_EXT = re.compile(r"\.(mp4|m3u8|mpd|webm)(\?|$)", re.I)
    BAD_HOST = ("googlesyndication.com", "doubleclick.net", "googletagmanager.com", "adpushup.com")
    def __init__(self, **kwargs):
        super(OrientalDailyVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36', "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ms;q=0.7"}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_walkjson'''
    def _walkjson(self, x):
        if isinstance(x, dict):
            yield x
            for v in x.values(): yield from self._walkjson(v)
        elif isinstance(x, list):
            for v in x: yield from self._walkjson(v)
    '''_jsonldvalues'''
    def _jsonldvalues(self, soup: BeautifulSoup, *keys):
        vals = []
        for tag in soup.select('script[type*="ld+json"]'):
            try: data = json.loads(tag.get_text(strip=True))
            except Exception: continue
            vals.extend(obj[k] for obj in self._walkjson(data) for k in keys if isinstance(obj, dict) and obj.get(k))
        return vals
    '''_jsstring'''
    def _jsstring(self, s: str):
        try: return json.loads('"' + s + '"')
        except Exception: return html.unescape(s.replace("\\/", "/").replace("\\u0025", "%").replace("\\u0026", "&"))
    '''_extractvideoinfo'''
    def _extractvideoinfo(self, html_text: str, page_url: str, request_overrides: dict = None) -> dict:
        clean_func, soup, direct, embeds = lambda s: re.sub(r"\s+", " ", html.unescape(str(s or ""))).strip(), BeautifulSoup(html_text, "lxml"), [], []
        norm_url_func = lambda u, base: (lambda u: urljoin(base, u) if u else "")(clean_func(u).replace("\\/", "/"))
        uniq_func = lambda xs: (lambda seen=set(): [seen.add(x) or x for x in xs if x and x not in seen])()
        meta_func = lambda soup, *names: next((clean_func(tag["content"]) for name in names for tag in ((soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name}) or soup.find("meta", attrs={"itemprop": name})),) if isinstance(tag, Tag) and tag.get("content")), "") if isinstance(soup, (BeautifulSoup, Tag)) else ""
        clean_title_func = lambda s: (lambda s: re.sub(r"\s*[|｜-]\s*(视频|國內|国内|国际|財經|财经|社会|娱乐|生活|体育|评论|地方|专题)\s*$", "", s).strip())(re.sub(r"\s*[|｜-]\s*(東方網|东方网|馬來西亞東方日報|马来西亚东方日报).*$", "", clean_func(s)))
        bad_video_url_func = lambda u: (lambda host: "blank.mp4" in u or any(x in host for x in OrientalDailyVideoClient.BAD_HOST))(urlparse(str(u)).netloc.lower())
        title = clean_title_func((soup.find("h1") and soup.find("h1").get_text(" ", strip=True)) or meta_func(soup, "og:title", "twitter:title") or (soup.title and soup.title.get_text(" ", strip=True)) or next(iter(self._jsonldvalues(soup, "headline", "name")), ""))
        cover = norm_url_func(meta_func(soup, "og:image:secure_url", "og:image", "twitter:image") or next(iter(self._jsonldvalues(soup, "thumbnailUrl", "image")), ""), page_url)
        selectors = ("#story-stream .video iframe[src], #story-stream .video video[src], " "#story-stream .video source[src], #story-stream .inline-media iframe[src], " ".story-stream-block .video iframe[src], .story-stream-block .video video[src], " "video[src], source[src]")
        for tag in soup.select(selectors):
            if not (src := norm_url_func(tag.get("src") or tag.get("data-src"), page_url)) or bad_video_url_func(src): continue
            (direct if OrientalDailyVideoClient.VIDEO_EXT.search(src) else embeds).append(src)
            if not cover and tag.get("poster"): cover = norm_url_func(tag.get("poster"), page_url)
        for v in self._jsonldvalues(soup, "contentUrl", "embedUrl", "url"):
            if (v := norm_url_func(v, page_url)) and not bad_video_url_func(v): direct.append(v) if OrientalDailyVideoClient.VIDEO_EXT.search(v) else embeds.append(v)
        for iframe in embeds:
            if "facebook.com/plugins/video" in iframe:
                (headers := self.default_headers.copy()).update({'Referer': page_url})
                (resp := self.get(iframe, headers=headers, **(request_overrides or {}))).raise_for_status()
                resp.encoding = resp.apparent_encoding or resp.encoding; urls = []
                for key in ("hd_src", "sd_src", "browser_native_hd_url", "browser_native_sd_url", "playable_url_quality_hd", "playable_url"):
                    pattern = r'"%s"\s*:\s*"((?:\\.|[^"\\])*)"' % re.escape(key)
                    urls += [self._jsstring(m.group(1)) for m in re.finditer(pattern, resp.text)]
                if not urls: urls += [self._jsstring(m.group(0)) for m in re.finditer(r"https?:\\?/\\?/[^\"'<> ]+?\.mp4[^\"'<> ]*", resp.text)]
                direct += uniq_func(u for u in urls if str(u).startswith("http") and not bad_video_url_func(u))
        direct, embeds = uniq_func(direct), uniq_func(embeds)
        return {"title": title, "cover_url": cover, "video_url": direct[0] if direct else (embeds[0] if embeds else ""), "videos": direct, "embeds": embeds}
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid = urlparse(url=url).path.strip('/').split('/')[-1].removesuffix('.html').removesuffix('.htm')
            (resp := self.get(url, **request_overrides)).raise_for_status(); resp.encoding = resp.apparent_encoding or 'utf-8'
            video_info.update(dict(raw_data=(raw_data := self._extractvideoinfo(resp.text, resp.url)))); video_info.update(dict(download_url=raw_data['video_url']))
            video_title = legalizestring(video_info.raw_data.get('title') or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies, skip_urllib_parse=True)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=video_info.raw_data.get('cover_url')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"orientaldaily.com.my", "odn.my"}
        return BaseVideoClient.belongto(url, valid_domains)