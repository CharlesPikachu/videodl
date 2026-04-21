'''
Function:
    Implementation of M1905VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import os
import copy
import time
import math
import random
import hashlib
import json_repair
from bs4 import BeautifulSoup
from urllib.parse import quote
from .base import BaseVideoClient
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, safeextractfromdict, taskprogress, VideoInfo


'''M1905VideoClient'''
class M1905VideoClient(BaseVideoClient):
    source = 'M1905VideoClient'
    class VideoTypes:
        MOVIE = "MOV"; TV = "TV"; CARTOON = "Cartoon"; SPORTS = "Sports"; ENTMT = "Ent"; GAME = "Game"; DOCU = "Docu"; VARIETY = "Variety"; MUSIC = "Music"; NEWS = "News"; FINANCE = "Finance"
        FASHION = "Fashion"; TRAVEL = "Travel"; EDUCATION = "Edu"; TECH = "Tech"; AUTO = "Auto"; HOUSE = "House"; LIFE = "Life"; FUN = "Fun"; BABY = "Baby"; CHILD = "Child"; ART = "Art"
    VIDEO_URL_PATS = [{'pat': r'^https?://www\.1905\.com/(?:vod|video)/play/(\d+)\.shtml', 'eg': 'https://www.1905.com/vod/play/1287886.shtml'}, {'pat': r'^https?://www\.1905\.com/mdb/film/(\d+)/?', 'eg': 'https://www.1905.com/mdb/film/2245563'}, {'pat': r'^https?://vip\.1905\.com/play/(\d+)\.shtml', 'eg': 'https://vip.1905.com/play/535547.shtml'}]
    VIDEO_URL_PATS = [re.compile(p['pat'], re.IGNORECASE) for p in VIDEO_URL_PATS]
    M1905_DEFINITION = {'free': ['uhd', 'hd', 'sd'], 'vip': ['v1080pm3u8', 'ipad800kbm3u8', 'm3u8ipad', 'm3u8iphone']}
    M1905_DEFN_MAP_I2S = {'free': {'uhd': 'shd', 'hd': 'hd', 'sd': 'sd'}, 'vip': {'v1080pm3u8': 'fhd', 'ipad800kbm3u8': 'shd', 'm3u8ipad': 'hd', 'm3u8iphone': 'sd'}}
    M1905_DEFN_MAP_S2I = {'free': {'dolby': 'uhd', 'suhd': 'uhd', 'hdr10': 'uhd', 'uhd': 'uhd', 'fhd': 'uhd', 'shd': 'uhd', 'hd': 'hd', 'sd': 'sd'}, 'vip': {'dolby': 'v1080pm3u8', 'suhd': 'v1080pm3u8', 'hdr10': 'v1080pm3u8', 'uhd': 'v1080pm3u8', 'fhd': 'v1080pm3u8', 'shd': 'ipad800kbm3u8', 'hd': 'm3u8ipad', 'sd': 'm3u8iphone'}}
    SD_CONF_PAT_RE = re.compile(r"(?:VODCONFIG|VIDEOCONFIG).*vid\s*:\s*\"(?P<vid>\d+)\".*?(?<!vip)title\s*:\s*\"(?P<title>.*?)\".*?apikey\s*:\s*\"(?P<apikey>.*?)\"", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    SD_YEAR_RE = re.compile(r"playerBox-info-year.*?\(\s*(\d+)\s*\)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    HD_MV_CONF_PAT_RE = re.compile(r"movie-title\s*\"\s*>(?P<title>[^<]+)</h1>.*?年份[^\d]+(?P<year>\d+).*?www\.1905\.com/mdb/film/(?P<cover_id>\d+)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    HD_TV_CONF_PAT_RE = re.compile(r"(?<!<!--)<h4\s+class=\"tv_title\">(?P<title>[^<]+)</h4>.*?年份[^\d]+(?P<year>\d+).+?CONFIG\['vipid'\][^\d]+(?P<cover_id>\d+)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    HD_TV_COVER_RE = re.compile(r"<div\s+id=\"dramaList\">.+?(?P<dramalist><ul\s+.*?</ul>)\s*</div>", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    HD_TV_EPISODE_RE = re.compile(r"<li.+?is_free=\"(?P<free>\d)\".+?vip\.1905\.com/play/(?P<vid>\d+)\.shtml[^\d]+(?P<ep>\d+).+?</li>", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    COVER_YEAR_RE = re.compile(r"header-wrapper-h1.*?\(\s*(\d+)\s*\)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    ONLINE_COVER_RE = re.compile(r"class\s*=\s*\"\s*watch-online.+?正片.+?(<ul\s+class\s*=\s*\"watch-online-list.*?</ul>)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    ONLINE_EPISODE_RE = re.compile(r"<a\s+href\s*=\s*\"([^\"]+)\"\s+.*?class=\"online-list-time\s*\">(.*?)</span>", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    APP_ID = "dde3d61a0411511d"
    VIDEO_COVER_FORMAT = "https://www.1905.com/mdb/film/{}/video"
    PROFILE_CONFIG_URL = "https://profile.m1905.com/mvod/getVideoinfo.php"
    VIP_CONFIG_URL = "https://vip.1905.com/playerhtml5/formal"
    def __init__(self, **kwargs):
        super(M1905VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_randomstring'''
    def _randomstring(self):
        translate_func = lambda c: (lambda n: ("{:x}".format(n) if c == "x" else "{:x}".format((3 & n) | 8) if c == "y" else c))(math.floor(16 * random.random()))
        random.seed()
        return ''.join(map(translate_func, "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"))
    '''_randomplayerid'''
    def _randomplayerid(self):
        return self._randomstring().replace('-', '')[5: 20]
    '''_signature'''
    def _signature(self, params: dict, appid: str = "dde3d61a0411511d"):
        query, ks = "", sorted(params.keys())
        for k in ks:
            if k != "signature": q = k + "=" + quote(str(params[k]), safe=""); query += "&" + q if query else q
        return hashlib.sha1((query + "." + appid).encode("utf-8")).hexdigest()
    '''_getcoverinfosd'''
    def _getcoverinfosd(self, epurl, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        (resp := self.get(epurl, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'; year = ""
        image_url = re.search(r'thumb\s*:\s*"(.*?)"', resp.text)
        if image_url: image_url = image_url.group(1)
        year_match = M1905VideoClient.SD_YEAR_RE.search(resp.text)
        if year_match: year = year_match.group(1); conf_match = M1905VideoClient.SD_CONF_PAT_RE.search(resp.text[year_match.end(0):])
        else: conf_match = M1905VideoClient.SD_CONF_PAT_RE.search(resp.text)
        if not conf_match: return None
        api_key = conf_match.group('apikey')
        cover_id_match = re.search(r"mdbfilmid\s*:\s*\"(\d+)\"", conf_match.group(0), flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
        cover_id = cover_id_match.group(1) if cover_id_match else ""
        info = {'image_url': image_url, 'title': conf_match.group('title'), 'year': year, 'cover_id': cover_id, 'type': M1905VideoClient.VideoTypes.MOVIE, 'api_key': api_key, 'normal_ids': [dict(V=conf_match.group('vid'), E=1, defns={}, free=True, vip=False, url=epurl)]}
        return info
    '''_getcoverinfohd'''
    def _getcoverinfohd(self, epurl, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        (resp := self.get(epurl, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'
        image_url = next((m.get('content') for m in BeautifulSoup(resp.text, 'html.parser').find_all('meta', attrs={'property': 'og:image'}) if m.get('content')), None)
        conf_match = M1905VideoClient.HD_MV_CONF_PAT_RE.search(resp.text)
        if conf_match: info = {'image_url': image_url, 'title': conf_match.group('title'), 'year': conf_match.group('year'), 'cover_id': conf_match.group('cover_id'), 'type': M1905VideoClient.VideoTypes.MOVIE, 'api_key': '', 'normal_ids': [dict(V=epurl.split('/')[-1].split('.')[0], E=1, defns={}, free=False, vip=True, url=epurl)]}
        else:
            cover_match = M1905VideoClient.HD_TV_COVER_RE.search(resp.text)
            if not cover_match: return None
            conf_match = M1905VideoClient.HD_TV_CONF_PAT_RE.search(resp.text[cover_match.end(0):])
            episodes_match = M1905VideoClient.HD_TV_EPISODE_RE.finditer(cover_match.group('dramalist'))
            if not (conf_match and episodes_match): return None
            info = {'image_url': image_url, 'title': conf_match.group('title'), 'year': conf_match.group('year'), 'cover_id': conf_match.group('cover_id'), 'type': M1905VideoClient.VideoTypes.TV, 'api_key': '', 'normal_ids': [dict(V=mo.group('vid'), E=int(mo.group('ep')), defns={}, free=bool(int(mo.group('free'))), vip=True, url="https://vip.1905.com/play/%s.shtml" % mo.group('vid')) for mo in episodes_match]}
        return info
    '''_getcoverinfo'''
    def _getcoverinfo(self, cvurl, request_overrides: dict = None):
        request_overrides, defns, year, urls = request_overrides or {}, {"VIP免广告": "hd", "免费": "sd"}, "", None
        (resp := self.get(cvurl, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'
        year_match = M1905VideoClient.COVER_YEAR_RE.search(resp.text)
        if year_match: year = year_match.group(1); cover_match = M1905VideoClient.ONLINE_COVER_RE.search(resp.text[year_match.end(0):])
        else: cover_match = M1905VideoClient.ONLINE_COVER_RE.search(resp.text)
        if cover_match: episodes_match = M1905VideoClient.ONLINE_EPISODE_RE.finditer(cover_match.group(1)); urls = {defns[mo.group(2)]: mo.group(1) for mo in episodes_match}
        return year, urls
    '''_getvideocoverinfo'''
    def _getvideocoverinfo(self, url, request_overrides: dict = None):
        for typ, pat in enumerate(M1905VideoClient.VIDEO_URL_PATS, 1):
            if not (match := pat.match(url)): continue
            if typ == 1: cover_info = self._getcoverinfosd(url, request_overrides)
            elif typ == 2: urls_dict = self._getcoverinfo(M1905VideoClient.VIDEO_COVER_FORMAT.format(match.group(1)), request_overrides)[-1]; cover_info = (self._getcoverinfohd(urls_dict["hd"], request_overrides) if urls_dict and urls_dict.get("hd") and (self.default_cookies or not urls_dict.get("sd")) else self._getcoverinfosd(urls_dict["sd"], request_overrides) if urls_dict and urls_dict.get("sd") else None)
            else: cover_info = self._getcoverinfohd(url, request_overrides); cover_info = (self._getcoverinfosd(urls_dict["sd"], request_overrides) if cover_info and cover_info["type"] == M1905VideoClient.VideoTypes.MOVIE and not self.default_cookies and (urls_dict := self._getcoverinfo(M1905VideoClient.VIDEO_COVER_FORMAT.format(cover_info["cover_id"]), request_overrides)[-1]) and urls_dict.get("sd") else cover_info)
            if not cover_info: return cover_info
            cover_info['url'] = url; cover_info['referrer'] = url; cover_info['episode_all'] = len(cover_info['normal_ids'])
            if cover_info['type'] == M1905VideoClient.VideoTypes.TV: video_id = match.group(1); cover_info['normal_ids'] = [dic for dic in cover_info['normal_ids'] if dic['V'] == video_id]
            return cover_info
    '''_updatevideodwnldinfosd'''
    def _updatevideodwnldinfosd(self, vi, request_overrides: dict = None):
        nonce, request_overrides = math.floor(time.time()), request_overrides or {}
        params = {'cid': vi['V'], 'expiretime': nonce + 600, 'nonce': nonce, 'page': vi['url'], 'playerid': self._randomplayerid(), 'type': "hls", 'uuid': self._randomstring()}
        params['signature'] = self._signature(params, M1905VideoClient.APP_ID)
        (resp := self.get(M1905VideoClient.PROFILE_CONFIG_URL, params=params, **request_overrides)).raise_for_status()
        if not (data := json_repair.loads(resp.text[len("null("): -1]).get('data')) or not isinstance(data, dict): return
        preferred_defn = M1905VideoClient.M1905_DEFN_MAP_S2I['free']["uhd"]
        for defn in ([preferred_defn] + [defn for defn in M1905VideoClient.M1905_DEFINITION['free'] if defn != preferred_defn]):
            host = safeextractfromdict(data, ['quality', defn, 'host'], None); sign = safeextractfromdict(data, ['sign', defn, 'sign'], None); path = safeextractfromdict(data, ['path', defn, 'path'], None)
            if not (host and path): continue
            if sign: playlist_m3u8 = str(host + sign + path).replace('\\', '')
            elif 'sign=' in path: playlist_m3u8 = str(host + path).replace('\\', '')
            else: continue
            vi["defns"] = [{M1905VideoClient.M1905_DEFN_MAP_I2S['free'][defn]: playlist_m3u8}]
    '''_updatevideodwnldinfohd'''
    def _updatevideodwnldinfohd(self, vi, request_overrides: dict = None):
        params, request_overrides = {'vipid': vi['V'], 'playerid': self._randomplayerid(), 'uuid': self._randomstring(), 'callback': 'fnCallback0'}, request_overrides or {}
        (resp := self.get(M1905VideoClient.VIP_CONFIG_URL, params=params, **request_overrides)).raise_for_status()
        data = json_repair.loads(resp.text[len("fnCallback0("): -1]).get('data')
        if not data or not isinstance(data, dict): return
        defn = M1905VideoClient.M1905_DEFN_MAP_S2I['vip']["uhd"]
        for defn in ([defn] if safeextractfromdict(data, ['path', defn], None) else M1905VideoClient.M1905_DEFINITION['vip']):
            if not (path := safeextractfromdict(data, ['path', defn], None)): continue
            playlist_m3u8 = str(path).replace('\\', '')
            vi["defns"] = [{M1905VideoClient.M1905_DEFN_MAP_I2S['vip'][defn]: playlist_m3u8}]
    '''_updatevideodwnldinfo'''
    def _updatevideodwnldinfo(self, vi, request_overrides: dict = None):
        if not vi['vip']: self._updatevideodwnldinfosd(vi, request_overrides)
        elif vi['free'] or self.default_cookies: self._updatevideodwnldinfohd(vi, request_overrides)
        else: raise RuntimeError(f"Couldn't download the VIP video from {vi['url']}. Please configure M1905VideoClient VIP cookies first.")
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title, video_infos = request_overrides or {}, VideoInfo(source=self.source, enable_nm3u8dlre=True), yieldtimerelatedtitle(self.source), []
        # try parse
        try:
            raw_data = self._getvideocoverinfo(url, request_overrides=request_overrides)
            with taskprogress(description='Possible Multiple Videos Detected >>> Parsing One by One', total=len((extracted_normal_ids := safeextractfromdict(raw_data, ['normal_ids'], [])))) as progress:
                for extracted_normal_id in extracted_normal_ids:
                    self._updatevideodwnldinfo(extracted_normal_id, request_overrides=request_overrides)
                    download_url = list(extracted_normal_id['defns'][0].values())[0]
                    (video_info_page := copy.deepcopy(video_info)).update(raw_data=raw_data, download_url=download_url)
                    video_title = legalizestring(raw_data['title'] or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                    video_title = f'EP{len(video_infos)+1}-{video_title}' if len(raw_data['normal_ids']) > 1 else video_title
                    video_info_page.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.m3u8'), ext='mp4', identifier=extracted_normal_id["V"], cover_url=raw_data.get('image_url'))); video_infos.append(video_info_page); progress.advance(1)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"1905.com"}
        return BaseVideoClient.belongto(url, valid_domains)