'''
Function:
    Implementation of DongchediVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import json_repair
from bs4 import BeautifulSoup
from .base import BaseVideoClient
from urllib.parse import urlparse, urlunparse
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, FileTypeSniffer, VideoInfo, DrissionPageUtils


'''DongchediVideoClient'''
class DongchediVideoClient(BaseVideoClient):
    source = 'DongchediVideoClient'
    def __init__(self, **kwargs):
        super(DongchediVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_converttomobileurl'''
    def _converttomobileurl(self, input_url: str) -> str:
        if not input_url: return input_url
        if not input_url.startswith("http://") and not input_url.startswith("https://"): input_url = "https://" + input_url
        try:
            parsed = urlparse(input_url)
            if parsed.hostname in ("www.dongchedi.com", "dongchedi.com"): parsed = parsed._replace(netloc=parsed.netloc.replace(parsed.hostname, "m.dongchedi.com")); return urlunparse(parsed)
            return input_url
        except Exception:
            return input_url
    '''_parsefromurlusingdrissionpage'''
    @useparseheaderscookies
    def _parsefromurlusingdrissionpage(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        url, request_overrides, video_info, null_backup_title, download_urls = self._converttomobileurl(url), request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []
        # try parse
        try:
            vid = urlparse(url).path.strip('/').split('/')[-1]
            page = DrissionPageUtils.initsmartbrowser(headless=True, requests_headers={"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}, requests_proxies=(request_overrides.get('proxies') or self._autosetproxies()), requests_cookies=(request_overrides.get('cookies') or self.default_cookies))
            page.set.window.size(390, 844); page.listen.start('vod.bytedanceapi.com'); page.get(url)
            try: page.ele('tag:body', timeout=2).click()
            except Exception: pass
            if (packet := page.listen.wait(timeout=8)) and packet.response and packet.response.body:
                if isinstance((body_data := packet.response.body), str): body_data = json_repair.loads(body_data)
                play_info_list: list[dict] = safeextractfromdict(body_data, ['Result', 'Data', 'PlayInfoList'], []) or []
                play_info_list.sort(key=lambda x: x.get('Bitrate', 0), reverse=True)
                for play_info in play_info_list:
                    if isinstance(play_info, dict) and (main_url := play_info.get('MainPlayUrl')) and main_url not in download_urls: download_urls.append(main_url); break
            page.listen.stop(); html_content = page.html; DrissionPageUtils.quitpage(page=page); download_url = download_urls[0]
            soup = BeautifulSoup(html_content, 'lxml'); script_tag = soup.find('script', id='__NEXT_DATA__')
            raw_data = json_repair.loads(script_tag.string); raw_data['drissionpage_download_urls'] = download_urls
            video_info.update(dict(raw_data=raw_data, download_url=download_url)); video_title, cover_url = null_backup_title, None
            for program in (safeextractfromdict(raw_data, ['props', 'pageProps', 'initEpisode', 'program_list'], []) or []):
                if isinstance(program, dict) and str(program.get('unique_id_str')) == str(vid): video_title = program.get('title'); cover_url = safeextractfromdict(program, ['video_info', 'cover_url'], None)
            video_title = legalizestring(video_title, replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlusingdrissionpage >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlusingdrissionpage]:
            video_infos = parser(url, request_overrides)
            if any(video_info.with_valid_download_url for video_info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"dongchedi.com"}
        return BaseVideoClient.belongto(url, valid_domains)