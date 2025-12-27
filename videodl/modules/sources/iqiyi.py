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
import math
import copy
import string
import random
import hashlib
from datetime import datetime
from .base import BaseVideoClient
from urllib.parse import urlencode, quote
from ..utils import legalizestring, useparseheaderscookies, resp2json, touchdir, FileTypeSniffer, VideoInfo


'''IQiyiVideoClient'''
class IQiyiVideoClient(BaseVideoClient):
    source = 'IQiyiVideoClient'
    def __init__(self, **kwargs):
        super(IQiyiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36', 
            'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'
        }
        self.default_download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''_calcsign'''
    def _calcsign(self, params: dict, secret_key: str = "howcuteitis"):
        query, ks = "", sorted(params.keys())
        for k in ks:
            q = k + "=" + str(params[k])
            query += q + "&"
        query = query[:-1]
        return hashlib.md5((query + "&secret_key=" + secret_key).encode("utf-8")).hexdigest().upper()
    '''_generatedeviceid'''
    def _generatedeviceid(self):
        random.seed()
        random_str = "".join(random.choices(string.printable, k=128))
        device_id = hashlib.md5(random_str.encode('utf-8')).hexdigest()
        return device_id
    '''_calcvf'''
    def _calcvf(self, url):
        def _ovappend(e):
            r = e
            for t in range(0, 4):
                for i in range(0, 2):
                    for n in range(0, 4):
                        a = (70 * t + 677 * i + 21 * n + 87 * t * i * n + 59) % 30
                        a += 48 if a < 9 else 88
                        r += chr(a)
            return r
        path_n_query = re.sub(r"^(https?://)?cache\.video\.iqiyi\.com", "", url, flags=re.IGNORECASE)
        return hashlib.md5(_ovappend(path_n_query).encode('utf-8')).hexdigest()
    '''_authkey'''
    def _authkey(self, tm, tvid):
        giveaway = hashlib.md5("".encode('utf-8')).hexdigest()
        return hashlib.md5((giveaway + str(tm) + str(tvid)).encode('utf-8')).hexdigest()
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        request_overrides = request_overrides or {}
        video_info = VideoInfo(source=self.source, enable_nm3u8dlre=True)
        if not self.belongto(url=url): return [video_info]
        device_id = self._generatedeviceid()
        # try parse
        try:
            # --tvid
            headers = copy.deepcopy(self.default_headers)
            headers.update({'referer': url})
            resp = self.get('https://mesh.if.iqiyi.com/player/lw/lwplay/accelerator.js?apiVer=3', headers=headers, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            tvid = re.compile(r"\"tvid\":\s*(?P<tvid>\d+)", re.MULTILINE | re.DOTALL | re.IGNORECASE).search(resp.text).group('tvid')
            # --basic info
            params = {
                'entity_id': int(tvid), 'device_id': device_id, 'auth_cookie': '', 'pcv': '13.062.22175', 'app_version': '13.062.22175',
                'ext': '', 'app_mode': 'standard', 'scale': 125, 'timestamp': int(time.time() * 1000), 'src': 'pca_tvg', 'os': '', 'conduit_id': ''
            }
            sign = self._calcsign(params)
            params['sign'] = sign
            resp = self.get('https://mesh.if.iqiyi.com/tvg/v2/lw/base_info', params=params, **request_overrides)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            raw_data = resp2json(resp=resp)
            # --video title
            dt = datetime.fromtimestamp(time.time())
            date_str = dt.strftime("%Y-%m-%d-%H-%M-%S")
            video_title = legalizestring(
                raw_data['data']['base_data'].get('title', f'{self.source}_null_{date_str}'), replace_null_string=f'{self.source}_null_{date_str}',
            ).removesuffix('.')
            # --dash
            data_details = raw_data['data']['template']['tabs'][0]['blocks'][2]['data']['data']
            # ----movie
            if isinstance(data_details, dict):
                normal_ids = [{'V': vi['qipu_id'], 'E': ep, 'defns': {}, 'title': vi.get('subtitle') or vi.get('title'), 'url': vi.get('page_url') or ''} for ep, vi in enumerate(data_details['videos'], start=1)]
            # ----tv
            else:
                videos = [vd['videos'] for vd in data_details if vd['videos'] and not isinstance(vd['videos'], str)][0]
                if isinstance(videos, dict):
                    vis = [vi for part, vi_lst in sorted(videos['feature_paged'].items(), key=lambda x: int(x[0].split('-')[0])) for vi in vi_lst]
                else:
                    vis = [vi for vd in sorted(videos, key=lambda x: int(x['title'].split('-')[0])) for vi in vd['data']]
                ep, normal_ids = 1, []
                for vi in vis:
                    if 0 < vi['album_order'] != ep: ep = vi['album_order']
                    normal_ids.append({'V': vi['qipu_id'], 'E': ep, 'defns': {}, 'title': vi.get('subtitle') or vi.get('title'), 'url': vi.get('page_url') or ''})
                    ep += 1
            # ----hit the target video rather than download all for tv
            vinfo_hit_tvid = [dic for dic in normal_ids if int(dic['V']) == int(tvid)][0]
            # ----parse download url from the highest resolution to lowest resolution
            qualities = {'dolby': 800, 'sfr_hdr': 800, 'hdr10': 800, 'uhd': 800, 'fhd': 600, 'shd': 500, 'hd': 300, 'sd': 200}
            tm, bid_tried = int(time.time() * 1000), set()
            for bid in list(qualities.values()):
                if bid in bid_tried: continue
                bid_tried.add(bid)
                params = {
                    'tvid': vinfo_hit_tvid['V'], 'bid': bid, 'vid': '', 'src': '01010031010000000000', 'vt': 0, 'rs': 1, 'uid': '', 'ori': 'pcw', 'ps': 1,
                    'k_uid': device_id, 'pt': 0, 'd': 0, 's': '', 'lid': 0, 'cf': 0, 'ct': 0, 'authKey': self._authkey(tm, vinfo_hit_tvid['V']), 'k_tag': 1, 'dfp': '',
                    'locale': 'zh_cn', 'pck': '', 'k_err_retries': 0, 'up': '', 'qd_v': 'a1', 'tm': tm, 'k_ft1': '706436220846084', 'k_ft4': '1162321298202628',
                    'k_ft5': '150994945', 'k_ft7': '4', 'fr_300': '120_120_120_120_120_120', 'fr_500': '120_120_120_120_120_120', 'fr_600': '120_120_120_120_120_120',
                    'fr_800': '120_120_120_120_120_120', 'fr_1020': '120_120_120_120_120_120', 'bop': quote('{"version":"10.0","dfp":"","b_ft1":28}'), 'sr': 1,
                    'ost': 0, 'ut': 0
                }
                params['vf'] = self._calcvf('/dash?' + urlencode(params))
                try:
                    resp = self.get('https://cache.video.iqiyi.com/dash', params=params, **request_overrides)
                    resp.raise_for_status()
                    resp.encoding = 'utf-8'
                    raw_data['cache.video.iqiyi.com/dash'] = resp2json(resp=resp)
                    video_info.update(dict(raw_data=raw_data))
                    vd = [vd for vd in sorted(raw_data['cache.video.iqiyi.com/dash']['data']['program']['video'], key=lambda x: x['bid'], reverse=True) if vd.get('m3u8') and vd['ff'] != 'dash'][0]
                    download_url = os.path.join(self.work_dir, self.source, f'{tvid}.m3u8')
                    touchdir(os.path.dirname(download_url))
                    with open(download_url, 'w') as fp: fp.write(vd['m3u8'])
                    video_info.update(download_url=download_url)
                    break
                except:
                    continue
            # --misc
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(
                url=download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies,
            )
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else video_info['ext']
            video_info.update(dict(
                title=video_title, file_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, 
                guess_video_ext_result=guess_video_ext_result, identifier=tvid,
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
    def belongto(url: str, valid_domains: list = None):
        if valid_domains is None:
            valid_domains = ["www.iqiyi.com"]
        return BaseVideoClient.belongto(url=url, valid_domains=valid_domains)