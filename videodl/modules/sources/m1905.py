'''
Function:
    Implementation of M1905VideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import math
import random
import hashlib
import json_repair
from .base import BaseVideoClient
from urllib.parse import urlparse, quote
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, FileTypeSniffer, VideoInfo


'''M1905VideoClient'''
class M1905VideoClient(BaseVideoClient):
    source = 'M1905VideoClient'
    def __init__(self, **kwargs):
        super(M1905VideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 
            'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_randomstring'''
    def _randomstring(self):
        def _translate(c):
            n = math.floor(16 * random.random())
            t = "{:x}".format(n) if 'x' == c else "{:x}".format(3 & n | 8) if 'y' == c else c
            return t
        random.seed()
        return ''.join(map(_translate, "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"))
    '''_randomplayerid'''
    def _randomplayerid(self):
        return self._randomstring().replace('-', '')[5: 20]
    '''_signature'''
    def _signature(self, params: dict, appid: str = "dde3d61a0411511d"):
        query, ks = "", sorted(params.keys())
        for k in ks:
            if k != "signature":
                q = k + "=" + quote(str(params[k]), safe="")
                query += "&" + q if query else q
        return hashlib.sha1((query + "." + appid).encode("utf-8")).hexdigest()
    '''_parsebasicinfo'''
    def _parsebasicinfo(self, cvurl, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        defns, year = {"VIP免广告": "hd", "免费": "sd"}, ""
        resp = self.get(cvurl, **request_overrides)
        resp.encoding = 'utf-8'
        html_str = resp.text
        year_match = re.compile(r"header-wrapper-h1.*?\(\s*(\d+)\s*\)", re.MULTILINE | re.DOTALL | re.IGNORECASE).search(resp.text)
        if year_match:
            year = year_match.group(1)
            html_str = html_str[year_match.end(0):]
        cover_match = re.compile(
            r"class\s*=\s*\"\s*watch-online.+?正片.+?(<ul\s+class\s*=\s*\"watch-online-list.*?</ul>)", re.MULTILINE | re.DOTALL | re.IGNORECASE
        ).search(html_str)
        episodes_match = re.compile(
            r"<a\s+href\s*=\s*\"([^\"]+)\"\s+.*?class=\"online-list-time\s*\">(.*?)</span>", re.MULTILINE | re.DOTALL | re.IGNORECASE
        ).finditer(cover_match.group(1))
        urls = {defns[mo.group(2)]: mo.group(1) for mo in episodes_match}
        return year, urls
    '''_parsesdbasicinfo'''
    def _parsesdbasicinfo(self, epurl: str, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        resp = self.get(epurl, **request_overrides)
        resp.raise_for_status()
        resp.encoding, year = 'utf-8', ""
        html_str = resp.text
        year_match = re.compile(r"playerBox-info-year.*?\(\s*(\d+)\s*\)", re.MULTILINE | re.DOTALL | re.IGNORECASE).search(html_str)
        if year_match:
            year = year_match.group(1)
            html_str = html_str[year_match.end(0):]
        conf_pattern = re.compile(r"(?:VODCONFIG|VIDEOCONFIG).*vid\s*:\s*\"(?P<vid>\d+)\".*?(?<!vip)title\s*:\s*\"(?P<title>.*?)\".*?apikey\s*:\s*\"(?P<apikey>.*?)\"", re.MULTILINE | re.DOTALL | re.IGNORECASE)
        conf_match = conf_pattern.search(html_str)
        api_key = conf_match.group('apikey')
        cover_id_match = re.search(r"mdbfilmid\s*:\s*\"(\d+)\"", conf_match.group(0), flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
        cover_id = cover_id_match.group(1) if cover_id_match else ""
        basic_info = {
            'title': conf_match.group('title'), 'year': year, 'cover_id': cover_id, 'type': 'MOVIE', 'api_key': api_key,
            'normal_ids': [dict(V=conf_match.group('vid'), E=1, defns={}, free=True, vip=False, url=epurl)]
        }
        return basic_info
    '''_parsehdbasicinfo'''
    def _parsehdbasicinfo(self, epurl: str, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        resp = self.get(epurl, **request_overrides)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        pattern = re.compile(
            r"movie-title\s*\"\s*>(?P<title>[^<]+)</h1>.*?年份[^\d]+(?P<year>\d+).*?www\.1905\.com/mdb/film/(?P<cover_id>\d+)", re.MULTILINE | re.DOTALL | re.IGNORECASE
        )
        conf_match = pattern.search(resp.text)
        if conf_match:
            basic_info = {
                'title': conf_match.group('title'), 'year': conf_match.group('year'), 'cover_id': conf_match.group('cover_id'), 'type': 'MOVIE', 'api_key': '',
                'normal_ids': [dict(V=epurl.split('/')[-1].split('.')[0], E=1, defns={}, free=False, vip=True, url=epurl)]
            }
        else:
            cover_match = re.compile(r"<div\s+id=\"dramaList\">.+?(?P<dramalist><ul\s+.*?</ul>)\s*</div>", re.MULTILINE | re.DOTALL | re.IGNORECASE).search(resp.text)
            pattern1 = re.compile(r"(?<!<!--)<h4\s+class=\"tv_title\">(?P<title>[^<]+)</h4>.*?年份[^\d]+(?P<year>\d+).+?CONFIG\['vipid'\][^\d]+(?P<cover_id>\d+)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
            pattern2 = re.compile(r"<li.+?is_free=\"(?P<free>\d)\".+?vip\.1905\.com/play/(?P<vid>\d+)\.shtml[^\d]+(?P<ep>\d+).+?</li>", re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if cover_match:
                conf_match = pattern1.search(resp.text[cover_match.end(0):])
                episodes_match = pattern2.finditer(cover_match.group('dramalist'))
                if conf_match and episodes_match:
                    basic_info = {
                        'title': conf_match.group('title'), 'year': conf_match.group('year'), 'cover_id': conf_match.group('cover_id'), 'type': 'TV', 'api_key': '',
                        'normal_ids': [dict(V=mo.group('vid'), E=int(mo.group('ep')), defns={}, free=bool(int(mo.group('free'))), vip=True, url="https://vip.1905.com/play/%s.shtml" % mo.group('vid')) for mo in episodes_match],
                    }
        return basic_info
    '''_parsesddownloadinfo'''
    def _parsesddownloadinfo(self, vi, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        nonce = math.floor(time.time())
        params = {
            'cid': vi['V'], 'expiretime': nonce + 600, 'nonce': nonce, 'page': vi['url'], 'playerid': self._randomplayerid(),
            'type': "hls", 'uuid': self._randomstring()
        }
        params['signature'] = self._signature(params)
        resp = self.get("https://profile.m1905.com/mvod/getVideoinfo.php", params=params, **request_overrides)
        resp.raise_for_status()
        data = json_repair.loads(resp.text[len("null("): -1]).get('data')
        qualities, qualities_tried = {
            'free': {'dolby': 'uhd', 'sfr_hdr': 'uhd', 'hdr10': 'uhd', 'uhd': 'uhd', 'fhd': 'uhd', 'shd': 'uhd', 'hd': 'hd', 'sd': 'sd'},
            'vip': {'dolby': 'v1080pm3u8', 'sfr_hdr': 'v1080pm3u8', 'hdr10': 'v1080pm3u8', 'uhd': 'v1080pm3u8', 'fhd': 'v1080pm3u8', 'shd': 'ipad800kbm3u8', 'hd': 'm3u8ipad', 'sd': 'm3u8iphone'}
        }['free'], set()
        for quality in list(qualities.values()):
            if quality in qualities_tried: continue
            qualities_tried.add(quality)
            try:
                host: str = data['quality'][quality]['host']
                sign: str = data['sign'][quality]['sign']
                path: str = data['path'][quality]['path']
                assert host and path
                if sign: download_url = (host + sign + path).replace('\\', '')
                elif 'sign=' in path: download_url = (host + path).replace('\\', '')
                else: raise Exception
                break
            except:
                continue
        return data, download_url
    '''_parsehddownloadinfo'''
    def _parsehddownloadinfo(self, vi, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        params = {
            'vipid': vi['V'], 'playerid': self._randomplayerid(), 'uuid': self._randomstring(), 'callback': 'fnCallback0'
        }
        resp = self.get("https://vip.1905.com/playerhtml5/formal", params=params, **request_overrides)
        resp.raise_for_status()
        data = json_repair.loads(resp.text[len("fnCallback0("): -1]).get('data')
        qualities, qualities_tried = {
            'free': {'dolby': 'uhd', 'sfr_hdr': 'uhd', 'hdr10': 'uhd', 'uhd': 'uhd', 'fhd': 'uhd', 'shd': 'uhd', 'hd': 'hd', 'sd': 'sd'},
            'vip': {'dolby': 'v1080pm3u8', 'sfr_hdr': 'v1080pm3u8', 'hdr10': 'v1080pm3u8', 'uhd': 'v1080pm3u8', 'fhd': 'v1080pm3u8', 'shd': 'ipad800kbm3u8', 'hd': 'm3u8ipad', 'sd': 'm3u8iphone'}
        }['vip'], set()
        for quality in list(qualities.values()):
            if quality in qualities_tried: continue
            qualities_tried.add(quality)
            try:
                download_url: str = data['path'][quality]
                assert download_url
                download_url = download_url.replace('\\', '')
                break
            except:
                continue
        return data, download_url
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if not self.belongto(url=url): return [video_info]
        null_backup_title = yieldtimerelatedtitle(self.source)
        patterns = [r'^https?://www\.1905\.com/(?:vod|video)/play/(\d+)\.shtml', r'^https?://www\.1905\.com/mdb/film/(\d+)/?', r'^https?://vip\.1905\.com/play/(\d+)\.shtml']
        patterns = [re.compile(pat, re.IGNORECASE) for pat in patterns]
        # try parse
        try:
            parsed_url = urlparse(url)
            vid = parsed_url.path.strip('/').split('.')[0]
            for typ, pat in enumerate(patterns, 1):
                m = pat.match(url)
                if not m: continue
                if typ == 1:
                    basic_info = self._parsesdbasicinfo(url, request_overrides=request_overrides)
                elif typ == 2:
                    year, urls_dict = self._parsebasicinfo("https://www.1905.com/mdb/film/{}/video".format(m.group(1)), request_overrides=request_overrides)
                    if urls_dict.get('hd') and (self.default_cookies or not urls_dict.get('sd')): basic_info = self._parsehdbasicinfo(urls_dict['hd'], request_overrides=request_overrides)
                    elif urls_dict.get('sd'): basic_info = self._parsesdbasicinfo(urls_dict['sd'], request_overrides=request_overrides)
                else:
                    assert typ == 3
                    basic_info = self._parsehdbasicinfo(url, request_overrides=request_overrides)
                    if basic_info and basic_info['type'] == 'MOVIE' and not self.default_cookies:
                        _, urls_dict = self._parsebasicinfo("https://www.1905.com/mdb/film/{}/video".format(basic_info['cover_id']), request_overrides=request_overrides)
                        if urls_dict and urls_dict.get('sd'): basic_info = self._parsesdbasicinfo(urls_dict['sd'], request_overrides=request_overrides)
                normal_ids = basic_info['normal_ids']
                if basic_info['type'] == "TV": normal_ids = [dic for dic in basic_info['normal_ids'] if dic['V'] == m.group(1)]
                vinfo_hit_vid = normal_ids[0]
                break
            if not vinfo_hit_vid['vip']: download_info, download_url = self._parsesddownloadinfo(vinfo_hit_vid, request_overrides=request_overrides)
            elif vinfo_hit_vid['free'] or self.default_cookies: download_info, download_url = self._parsehddownloadinfo(vinfo_hit_vid, request_overrides=request_overrides)
            raw_data = basic_info
            raw_data['download_info'] = download_info
            video_info.update(dict(raw_data=raw_data))
            video_info.update(dict(download_url=download_url))
            video_title = legalizestring(raw_data.get('title', null_backup_title), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid,
            ))
        except Exception as err:
            err_msg = f'{self.source}.parsefromurl >>> {url} (Error: {err})'
            video_info.update(dict(err_msg=err_msg))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # construct video infos
        video_infos = [video_info]
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"1905.com"}
        return BaseVideoClient.belongto(url, valid_domains)