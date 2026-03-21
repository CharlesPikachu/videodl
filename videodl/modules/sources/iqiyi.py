'''
Function:
    Implementation of IQiyiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import re
import time
import copy
import string
import random
import hashlib
from .base import BaseVideoClient
from urllib.parse import urlencode, quote
from ..utils.domains import IQIYI_SUFFIXES
from ..utils import legalizestring, useparseheaderscookies, resp2json, touchdir, yieldtimerelatedtitle, safeextractfromdict, VideoInfo


'''IQiyiVideoClient'''
class IQiyiVideoClient(BaseVideoClient):
    source = 'IQiyiVideoClient'
    class VideoTypes:
        MOVIE = "MOV"; TV = "TV"; CARTOON = "Cartoon"; SPORTS = "Sports"; ENTMT = "Ent"; GAME = "Game"; DOCU = "Docu"; VARIETY = "Variety"; MUSIC = "Music"; NEWS = "News"; FINANCE = "Finance"
        FASHION = "Fashion"; TRAVEL = "Travel"; EDUCATION = "Edu"; TECH = "Tech"; AUTO = "Auto"; HOUSE = "House"; LIFE = "Life"; FUN = "Fun"; BABY = "Baby"; CHILD = "Child"; ART = "Art"
    IQIYI_DEFN_MAP_I2S = {800: 'uhd', 600: 'fhd', 500: 'shd', 300: 'hd', 200: 'sd'}
    IQIYI_DEFN_MAP_S2I = {'dolby': 800, 'suhd': 800, 'hdr10': 800, 'uhd': 800, 'fhd': 600, 'shd': 500, 'hd': 300, 'sd': 200}
    TVID_PAT_RE = re.compile(r"\"tvid\":\s*(?P<tvid>\d+)", re.MULTILINE | re.DOTALL | re.IGNORECASE)
    PLAYER_INIT_URL = 'https://mesh.if.iqiyi.com/player/lw/lwplay/accelerator.js?apiVer=3'
    VIDEO_COVER_PREFIX = 'https://mesh.if.iqiyi.com/tvg/v2/lw/base_info'
    VIDEO_CONFIG_URL = 'https://cache.video.iqiyi.com/dash'
    APP_VERSION = '13.062.22175'
    def __init__(self, **kwargs):
        super(IQiyiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_calcvf'''
    def _calcvf(self, url):
        ovappend_func = lambda e: e + ''.join(chr(((70*t + 677*i + 21*n + 87*t*i*n + 59) % 30) + (48 if ((70*t + 677*i + 21*n + 87*t*i*n + 59) % 30) < 9 else 88)) for t in range(4) for i in range(2) for n in range(4))
        path_n_query = re.sub(r"^(https?://)?cache\.video\.iqiyi\.com", "", url, flags=re.IGNORECASE)
        return hashlib.md5(ovappend_func(path_n_query).encode('utf-8')).hexdigest()
    '''_authkey'''
    def _authkey(self, tm, tvid):
        giveaway = hashlib.md5("".encode('utf-8')).hexdigest()
        return hashlib.md5((giveaway + str(tm) + str(tvid)).encode('utf-8')).hexdigest()
    '''_calcsign'''
    def _calcsign(self, params: dict, secret_key: str = "howcuteitis"):
        query, ks = "", sorted(params.keys())
        for k in ks: query += (k + "=" + str(params[k])) + "&"
        query = query[:-1]
        return hashlib.md5((query + "&secret_key=" + secret_key).encode("utf-8")).hexdigest().upper()
    '''_generatedeviceid'''
    def _generatedeviceid(self):
        random.seed()
        random_str = "".join(random.choices(string.printable, k=128))
        device_id = hashlib.md5(random_str.encode('utf-8')).hexdigest()
        return device_id
    '''_getvideocoverinfo'''
    def _getvideocoverinfo(self, url, device_id, request_overrides: dict = None):
        info, req_url, request_overrides = None, IQiyiVideoClient.PLAYER_INIT_URL, request_overrides or {}
        try:
            (resp := self.get(req_url, headers={'referer': url}, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'
            tvid = IQiyiVideoClient.TVID_PAT_RE.search(resp.text).group('tvid')
            params = {'entity_id': tvid, 'device_id': device_id, 'auth_cookie': '', 'pcv': IQiyiVideoClient.APP_VERSION, 'app_version': IQiyiVideoClient.APP_VERSION, 'ext': '', 'app_mode': 'standard', 'scale': 125, 'timestamp': int(time.time() * 1000), 'src': 'pca_tvg', 'os': '', 'conduit_id': ''}
            params['sign'] = self._calcsign(params)
            (resp := self.get(IQiyiVideoClient.VIDEO_COVER_PREFIX, params=params, **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'
            raw_data = resp2json(resp=resp); data = raw_data['data']
            image_url = safeextractfromdict(raw_data, ['data', 'base_data', 'image_url'], None)
            info = {'image_url': image_url, 'url': url, 'referrer': url, 'title': data['base_data']['title'], 'year': data['base_data']['current_video_year'], 'cover_id': data['base_data']['qipu_id'], 'type': IQiyiVideoClient.VideoTypes.MOVIE if data['base_data']['album_source_type'] == '-1' else IQiyiVideoClient.VideoTypes.TV}
            vi: dict = {'V': tvid, 'E': 1, 'defns': {}, 'url': url, 'referrer': url}; info['normal_ids'] = [vi]; info['episode_all'] = 1
            if not (data := safeextractfromdict(data, ['template', 'tabs', 0, 'blocks', 2, 'data', 'data'], None)): return info
            if isinstance(data, dict):
                info['normal_ids'] = [{'V': vi['qipu_id'], 'E': ep, 'defns': {}, 'title': vi.get('subtitle') or vi.get('title'), 'url': vi.get('page_url') or ''} for ep, vi in enumerate(data['videos'], start=1)]
            else:
                if not (videos := [vd['videos'] for vd in data if vd['videos'] and not isinstance(vd['videos'], str)]): return info
                videos, ep, normal_ids = videos[0], 1, []
                if isinstance(videos, dict): vis = [vi for part, vi_lst in sorted(videos['feature_paged'].items(), key=lambda x: int(x[0].split('-')[0])) for vi in vi_lst]
                else: vis = [vi for vd in sorted(videos, key=lambda x: int(x['title'].split('-')[0])) for vi in vd['data']]
                for vi in vis:
                    if 0 < vi['album_order'] != ep: ep = vi['album_order']
                    normal_ids.append({'V': vi['qipu_id'], 'E': ep, 'defns': {}, 'title': vi.get('subtitle') or vi.get('title'), 'url': vi.get('page_url') or ''}); ep += 1
                info['normal_ids'] = normal_ids
            info['episode_all'] = len(info['normal_ids'])
            info['normal_ids'] = [dic for dic in info['normal_ids'] if str(dic['V']) == str(tvid)]
            return info
        except: return info
    '''_updatevideodwnldinfo'''
    def _updatevideodwnldinfo(self, vi, device_id, request_overrides: dict = None):
        tm, request_overrides = int(time.time() * 1000), request_overrides or {}
        params = {'tvid': vi['V'], 'bid': IQiyiVideoClient.IQIYI_DEFN_MAP_S2I['uhd'], 'vid': '', 'src': '01010031010000000000', 'vt': 0, 'rs': 1, 'uid': '', 'ori': 'pcw', 'ps': 1, 'k_uid': device_id, 'pt': 0, 'd': 0, 's': '', 'lid': 0, 'cf': 0, 'ct': 0, 'authKey': self._authkey(tm, vi['V']), 'k_tag': 1, 'dfp': '', 'locale': 'zh_cn', 'pck': '', 'k_err_retries': 0, 'up': '', 'qd_v': 'a1', 'tm': tm, 'k_ft1': '706436220846084', 'k_ft4': '1162321298202628', 'k_ft5': '150994945', 'k_ft7': '4', 'fr_300': '120_120_120_120_120_120', 'fr_500': '120_120_120_120_120_120', 'fr_600': '120_120_120_120_120_120', 'fr_800': '120_120_120_120_120_120', 'fr_1020': '120_120_120_120_120_120', 'bop': quote('{"version":"10.0","dfp":"","b_ft1":28}'), 'sr': 1, 'ost': 0, 'ut': 0}
        params['vf'] = self._calcvf('/dash?' + urlencode(params))
        try:
            (resp := self.get(IQiyiVideoClient.VIDEO_CONFIG_URL + '?' + urlencode(params), **request_overrides)).raise_for_status(); resp.encoding = 'utf-8'
            raw_data = resp2json(resp=resp); data = raw_data['data']
            vd = [vd for vd in sorted(data['program']['video'], key=lambda x: x['bid'], reverse=True) if vd.get('m3u8') and vd['ff'] != 'dash'][0]
            ts_urls = [ts for ts in vd['m3u8'].split('\n') if ts and not ts.startswith('#')]
            std_defn = IQiyiVideoClient.IQIYI_DEFN_MAP_I2S[vd['bid']]
            vi["defns"].setdefault(std_defn, []).append(dict(ext=vd['ff'], urls=ts_urls))
            vi['highest_defns_original'] = vd['m3u8']
        except Exception: pass
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None) -> list[VideoInfo]:
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source, enable_nm3u8dlre=True), yieldtimerelatedtitle(self.source)
        device_id, video_infos = self._generatedeviceid(), []
        # try parse
        try:
            raw_data = self._getvideocoverinfo(url, device_id=device_id, request_overrides=request_overrides)
            for normal_id in raw_data['normal_ids']:
                self._updatevideodwnldinfo(normal_id, device_id=device_id, request_overrides=request_overrides)
                touchdir(os.path.dirname((download_url := os.path.join(self.work_dir, self.source, f'{normal_id["V"]}.m3u8'))))
                with open(download_url, 'w') as fp: fp.write(normal_id['highest_defns_original'])
                (video_info_page := copy.deepcopy(video_info)).update(raw_data=raw_data, download_url=download_url)
                video_title = legalizestring(normal_id['title'] or null_backup_title, replace_null_string=null_backup_title).removesuffix('.')
                video_title = f'ep{len(video_infos)+1}-{video_title}' if len(raw_data['normal_ids']) > 1 else video_title
                video_info_page.update(dict(title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.m3u8'), ext='mp4', identifier=normal_id["V"], cover_url=raw_data.get('image_url'))); video_infos.append(video_info_page)
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})'))); video_infos.append(video_info)
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return video_infos
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | IQIYI_SUFFIXES
        return BaseVideoClient.belongto(url, valid_domains)