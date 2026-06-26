'''
Function:
    Implementation of NewsPicksVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import html
import json
import urllib.parse
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo


'''NewsPicksVideoClient'''
class NewsPicksVideoClient(BaseVideoClient):
    source = 'NewsPicksVideoClient'
    def __init__(self, **kwargs):
        super(NewsPicksVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        extract_nextjs_data_func = lambda webpage: json.loads(html.unescape(re.search(r'<script[^>]+id=["\']__NEXT_DATA__["\'][^>]*>(?P<data>.*?)</script>', webpage, flags=re.DOTALL | re.IGNORECASE,).group("data")).strip())
        # try parse
        try:
            series_id = (re.match(r"https?://newspicks\.com/movie-series/(?P<series_id>[^?/#]+)", url)).group("series_id").rstrip("/")
            query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query); movie_ids = query.get("movieId")
            video_id = str(movie_ids[-1]); video_info.update(dict(raw_data=(raw_data := extract_nextjs_data_func(webpage=self.get(url, timeout=10, **request_overrides).text))))
            download_url = raw_data["props"]["pageProps"]["fragment"]['movie']['movieUrl']; video_info.update(dict(download_url=download_url))
            video_title = legalizestring(safeextractfromdict(raw_data["props"]["pageProps"]["fragment"], ['movie', 'title'], None) or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            cover_url = safeextractfromdict(raw_data["props"]["pageProps"]["fragment"]['movie'], ['image'], None) or safeextractfromdict(raw_data["props"]["pageProps"]["fragment"]['movie'], ['coverImageUrl'], None)
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=f'{series_id}-{video_id}', cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"newspicks.com"}
        return BaseVideoClient.belongto(url, valid_domains)