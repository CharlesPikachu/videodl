'''
Function:
    Implementation of RedditVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import copy
import json
import urllib.parse
from datetime import datetime
from .base import BaseVideoClient
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
from ..utils import legalizestring, useparseheaderscookies, resp2json, FileTypeSniffer, VideoInfo


'''RedditMediaInfo'''
@dataclass
class RedditMediaInfo:
    post_id: str
    display_id: str
    title: str
    alt_title: str
    subreddit: Optional[str]
    author: Optional[str]
    over_18: bool
    duration: Optional[int]
    video_id: Optional[str]
    hls_url: Optional[str]
    dash_url: Optional[str]
    fallback_url: Optional[str]
    is_playlist: bool = False
    playlist_items: Optional[List[Dict[str, Any]]] = None


'''RedditVideoClient'''
class RedditVideoClient(BaseVideoClient):
    source = 'RedditVideoClient'
    def __init__(self, **kwargs):
        super(RedditVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_initsession'''
    def _initsession(self):
        super()._initsession()
        self.session.cookies.set("over18", "1", domain=".reddit.com")
        options = {"pref_gated_sr_optin": True}
        self.session.cookies.set("_options", urllib.parse.quote(json.dumps(options)), domain=".reddit.com")
    '''_fetchpostjson'''
    def _fetchpostjson(self, url: str, request_overrides: dict = None) -> Any:
        request_overrides = request_overrides or {}
        api_url = url.rstrip("/") + "/.json"
        resp = self.get(api_url, allow_redirects=True, **request_overrides)
        resp.raise_for_status()
        return resp2json(resp=resp)
    '''_extractmediainfo'''
    def _extractmediainfo(self, url: str, request_overrides: dict = None) -> RedditMediaInfo:
        # basic parse
        request_overrides = request_overrides or {}
        js = self._fetchpostjson(url, request_overrides=request_overrides)
        data: dict = js[0]["data"]["children"][0]["data"]
        post_id, title = data.get("id") or "", data.get("title") or ""
        display_id, alt_title = data.get("name") or post_id, title
        subreddit, author, over_18, duration = data.get("subreddit"), data.get("author"), bool(data.get("over_18")), None
        # crosspost_parent_list
        cplist, reddit_video = data.get("crosspost_parent_list") or [], None
        for cp in cplist:
            if not isinstance(cp, dict): continue
            sm = cp.get("secure_media") or cp.get("media") or {}
            rv = sm.get("reddit_video")
            if rv: reddit_video = rv; break
        # secure_media/media
        if not reddit_video:
            sm = data.get("secure_media") or data.get("media") or {}
            reddit_video = sm.get("reddit_video")
        # multi videos perhaps
        hls_url = dash_url = fallback_url = video_id = None
        media_metadata, playlist_items = data.get("media_metadata") or {}, []
        if not reddit_video and media_metadata:
            for mid, meta in media_metadata.items():
                if not isinstance(meta, dict): continue
                if meta.get("e") != "RedditVideo": continue
                hls, dash = meta.get("hlsUrl"), meta.get("dashUrl")
                playlist_items.append({"id": mid, "hls_url": hls, "dash_url": dash})
        is_playlist = bool(playlist_items)
        # reddit_video
        if reddit_video:
            fallback_url, hls_url, dash_url, duration = reddit_video.get("fallback_url"), reddit_video.get("hls_url"), reddit_video.get("dash_url"), reddit_video.get("duration")
            if fallback_url:
                m = re.search(r"https?://v\.redd\.it/([^/?#&]+)", fallback_url)
                if m: video_id = m.group(1)
        elif is_playlist:
            video_id = None
        # return
        return RedditMediaInfo(
            post_id=post_id, display_id=display_id, title=title, alt_title=alt_title, subreddit=subreddit, author=author,
            over_18=over_18, duration=duration, video_id=video_id, hls_url=hls_url, dash_url=dash_url, fallback_url=fallback_url,
            is_playlist=is_playlist, playlist_items=playlist_items or None,
        )
    '''_augmenthlsquery'''
    def _augmenthlsquery(self, url: str) -> str:
        if not url: return url
        parsed = urllib.parse.urlparse(url)
        qs = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
        f = qs.get("f")
        if f:
            if "subsAll" not in f: f = f + ",subsAll"
        else:
            f = "hd,subsAll"
        qs["f"] = f
        new_query = urllib.parse.urlencode(qs)
        return urllib.parse.urlunparse(parsed._replace(query=new_query))
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source)
        if not self.belongto(url=url): return [video_info]
        # try parse
        video_infos = []
        try:
            media = self._extractmediainfo(url, request_overrides=request_overrides)
            if not media.hls_url and not media.dash_url and not media.is_playlist:
                post_js = self._fetchpostjson(url, request_overrides=request_overrides)
                data: dict = post_js[0]["data"]["children"][0]["data"]
                final_url = data.get("url")
                raise RuntimeError(f'The video in this post is not hosted on Reddit; it is an external link: {final_url}')
            if media.is_playlist and media.playlist_items:
                for idx, item in enumerate(media.playlist_items, 1):
                    hls_url, dash_url, vid = item.get("hls_url"), item.get("dash_url"), item["id"]
                    if hls_url: hls_url = self._augmenthlsquery(hls_url)
                    elif dash_url: hls_url = dash_url
                    if not hls_url: continue
                    dt = datetime.fromtimestamp(time.time())
                    date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
                    video_title = media.title or f'{self.source}_null_{date_str}'
                    video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
                    video_title = f'{video_title}_{idx}'
                    guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                        url=hls_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                    )
                    ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                    video_info_page = copy.deepcopy(video_info)
                    video_info_page.update(dict(
                        raw_data=item, download_url=hls_url, title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext,
                        guess_video_ext_result=guess_video_ext_result, identifier=vid, enable_nm3u8dlre=True
                    ))
                    video_infos.append(video_info_page)
            else:
                download_url = media.hls_url or media.dash_url
                if download_url: download_url = self._augmenthlsquery(download_url)
                elif media.fallback_url: download_url = media.fallback_url
                else: raise
                dt = datetime.fromtimestamp(time.time())
                date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
                video_title = media.title or f'{self.source}_null_{date_str}'
                video_title = legalizestring(video_title, replace_null_string=f'{self.source}_null_{date_str}').removesuffix('.')
                guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                    url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
                )
                ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
                video_info.update(dict(
                    raw_data=asdict(media), download_url=download_url, title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext,
                    guess_video_ext_result=guess_video_ext_result, identifier=media.post_id or media.display_id or download_url, enable_nm3u8dlre=True
                ))
                video_infos.append(video_info)
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.reddit.com", "old.reddit.com", "nm.reddit.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)