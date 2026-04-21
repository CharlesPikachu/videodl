'''
Function:
    Implementation of TBNUKVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import json_repair
from .base import BaseVideoClient
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, taskprogress, VideoInfo, FileTypeSniffer


'''TBNUKVideoClient'''
class TBNUKVideoClient(BaseVideoClient):
    source = 'TBNUKVideoClient'
    API_KEY = None
    BASE_URL = "https://watch.tbn.uk"
    STREAM_URL = '/api/{stream_type}/stream/{stream_id}'
    def __init__(self, **kwargs):
        super(TBNUKVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_setapiinfo'''
    def _setapiinfo(self, request_overrides: dict = None):
        if TBNUKVideoClient.API_KEY is not None: return
        (resp := self.get(TBNUKVideoClient.BASE_URL, **request_overrides)).raise_for_status()
        api_config = json_repair.loads(re.findall(r'config[^=]*=[^{]*({[^;]+});', resp.text)[0])["api"]
        TBNUKVideoClient.API_KEY = api_config["key"]
        TBNUKVideoClient.STREAM_URL = api_config["endpoints"]["streams"] + TBNUKVideoClient.STREAM_URL
    '''_parsefromurlwithwatch'''
    @useparseheaderscookies
    def _parsefromurlwithwatch(self, url: str, request_overrides: dict = None) -> list["VideoInfo"]:
        # prepare
        if (not self.belongto(url=url)) or (("/watch/vod/" not in url.split("?")[0].split("#")[0].rstrip("/")) and ("/watch/replay/" not in url.split("?")[0].split("#")[0].rstrip("/"))): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source); self._setapiinfo(request_overrides=request_overrides)
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0", "priority": "u=0, i", "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "document", "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
        # try parse
        try:
            vid = re.compile(r'https?://[^/]+/watch/(?:replay|vod)/(\d+)(?=[/?#]|$)').search(url).group(1)
            (resp := self.get(url, headers=headers, **request_overrides)).raise_for_status(); html_str = resp.text
            stream_type = str((re.findall(r"type[^:]*:[^']*'([^']+)'", (re.findall(r'this.url.params[^=]*=[^{]*({[^}]+})', html_str) or re.findall(r'programme[^{]*({[^}]+})', html_str))[0]))[0]).lower()
            (resp := self.post(TBNUKVideoClient.STREAM_URL.format(stream_type=stream_type, stream_id=vid), params={'key': TBNUKVideoClient.API_KEY, 'platform': 'chrome'}, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp)))); response: dict = raw_data['response']
            assert (not response.get('drm')) and ("not found" not in str(response.get("error", "")).lower())
            download_url = response.get("stream", "") if response.get("stream", "") not in ("", None) else (lambda ads: ads["prefix"] + json_repair.loads(self.post(ads["prefix"] + ads["session"], **request_overrides).text)["manifestUrl"])(response["ads"])
            try: video_title = legalizestring(BeautifulSoup(html_str, 'lxml').title.text or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            except Exception: video_title = legalizestring(null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(download_url=download_url, title=video_title)
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            cover_url = next((meta.get('content') for meta in BeautifulSoup(html_str, 'lxml').find_all('meta', property='og:image') if meta.get('content')), "")
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlwithwatch >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''_parsefromurlwithlive'''
    @useparseheaderscookies
    def _parsefromurlwithlive(self, url: str, request_overrides: dict = None) -> list["VideoInfo"]:
        # prepare
        if (not self.belongto(url=url)) or ("/live/" not in url.split("?")[0].split("#")[0].rstrip("/")): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source); self._setapiinfo(request_overrides=request_overrides)
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "accept-encoding": "gzip, deflate, br, zstd", "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "max-age=0", "priority": "u=0, i", "sec-ch-ua": '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"', "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"Windows"', "sec-fetch-dest": "document", "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate", "sec-fetch-user": "?1", "upgrade-insecure-requests": "1", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
        }
        # try parse
        try:
            vid = re.compile(r'https?://[^/]+/live/(\d+)(?=[/?#]|$)').search(url).group(1); stream_type = "live"
            (resp := self.get(url, headers=headers, **request_overrides)).raise_for_status(); html_str = resp.text
            (resp := self.post(TBNUKVideoClient.STREAM_URL.format(stream_type=stream_type, stream_id=vid), params={'key': TBNUKVideoClient.API_KEY, 'platform': 'chrome', 'url': url}, **request_overrides)).raise_for_status()
            video_info.update(dict(raw_data=(raw_data := resp2json(resp)))); response: dict = raw_data['response']
            assert (not response.get('drm')) and ("not found" not in str(response.get("error", "")).lower())
            download_url = response.get("stream", "") if response.get("stream", "") not in ("", None) else (lambda ads: ads["prefix"] + json_repair.loads(self.post(ads["prefix"] + ads["session"], **request_overrides).text)["manifestUrl"])(response["ads"])
            try: video_title = legalizestring(BeautifulSoup(html_str, 'lxml').title.text or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            except Exception: video_title = legalizestring(null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
            video_info.update(download_url=download_url, title=video_title)
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info.ext
            cover_url = next((meta.get('content') for meta in BeautifulSoup(html_str, 'lxml').find_all('meta', property='og:image') if meta.get('content')), "")
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=cover_url))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlwithlive >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''_parsefromurlwithshows'''
    @useparseheaderscookies
    def _parsefromurlwithshows(self, url: str, request_overrides: dict = None) -> list["VideoInfo"]:
        # prepare
        if (not self.belongto(url=url)) or ("/shows/" not in url.split("?")[0].split("#")[0].rstrip("/")): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source), []; self._setapiinfo(request_overrides=request_overrides)
        # try parse
        try:
            (resp := self.get(url, **request_overrides)).raise_for_status()
            try: collection_title = re.findall(r'"af_content"[^:]*:[^"]*"([^"]+)"', resp.text)[0]; assert len(collection_title) > 0
            except: collection_title = urlparse(url).path.strip('/').split('/')[-1]
            card_nodes, seasons = BeautifulSoup(resp.text, 'lxml').find_all('div', class_=lambda c: c and "card-body" in c), {}; card_nodes: list[Tag] = card_nodes
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len(card_nodes)) as progress:
                for card_node in card_nodes:
                    try:
                        assert len((episode_url := (card_title := card_node.find(class_=lambda c: c and "card-title" in c).find("a", attrs={"href": True}))["href"])) > 0
                        season_tag: Tag = card_node.find("span", attrs={"data-content-type": "season"})
                        season_index = int(re.search(r'season\s*(\d+)', season_tag.get_text().strip(), flags=re.IGNORECASE).group(1))
                        episode_tag: Tag = card_node.find("span", attrs={"data-content-type": "episode"})
                        episode_index = int(re.search(r'episode\s*(\d+)', episode_tag.get_text().strip(), flags=re.IGNORECASE).group(1))
                        try: assert len((episode_title := card_title.get_text().strip())) > 0
                        except Exception: episode_title = str(episode_url).split("/")[-1]
                        if seasons.get(season_index, None) is None: seasons[season_index] = []
                        video_info = self._parsefromurlwithwatch(episode_url, request_overrides=request_overrides)[0]
                        video_info.title = legalizestring(f'{collection_title} - EP{episode_index} - {episode_title}', replace_null_string=null_backup_title)
                        video_info.with_valid_download_url and video_infos.append(video_info)
                    except Exception as err: pass
                    finally: progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}._parsefromurlwithshows >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        for parser in [self._parsefromurlwithwatch, self._parsefromurlwithshows, self._parsefromurlwithlive]:
            video_infos = parser(url, request_overrides)
            if any(video_info.with_valid_download_url for video_info in (video_infos or [])): break
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"tbn.uk"}
        return BaseVideoClient.belongto(url, valid_domains)