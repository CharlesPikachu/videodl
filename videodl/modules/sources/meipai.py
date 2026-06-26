'''
Function:
    Implementation of MeipaiVideoClient
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import random
import urllib.parse
from hashlib import md5
from .base import BaseVideoClient
from urllib.parse import urlparse, unquote_plus
from ..utils import legalizestring, useparseheaderscookies, yieldtimerelatedtitle, resp2json, FileTypeSniffer, VideoInfo


'''MeipaiVideoClient'''
class MeipaiVideoClient(BaseVideoClient):
    source = 'MeipaiVideoClient'
    def __init__(self, **kwargs):
        super(MeipaiVideoClient, self).__init__(**kwargs)
        self.default_parse_headers = {'User-Agent': 'Meipai/9.7.900 (iPhone; iOS 26.5; Scale/3.00)', 'Ab-Version': '5.2.0', 'Ab-List': '1116', 'Accept-Language': 'zh-Hans-CN;q=1'}
        self.default_download_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'}
        self.default_headers = self.default_parse_headers
        self._initsession()
    '''getsig'''
    @staticmethod
    def getsig(params: dict, url_type='medias/show.json'):
        params_values = [unquote_plus(str(v)) for k, v in params.items() if 'sig' not in k]; params_values.sort()
        encry_params_str: str = url_type + ''.join(params_values) + 'bdaefd747c7d594f' + params['sigTime'] + 'Tw5AY783H@EU3#XC'
        params_md5_list = list(md5(encry_params_str.encode('utf-8')).hexdigest())
        for i in range(0, len(params_md5_list), 2): params_md5_list[i], params_md5_list[i + 1] = params_md5_list[i + 1], params_md5_list[i]
        return ''.join(params_md5_list)
    '''parsefromurl'''
    @useparseheaderscookies
    def parsefromurl(self, url: str, request_overrides: dict = None):
        # prepare
        if not self.belongto(url=url): return []
        request_overrides, video_info, null_backup_title = request_overrides or {}, VideoInfo(source=self.source), yieldtimerelatedtitle(self.source)
        # try parse
        try:
            vid, timestamp = urlparse(url).path.strip('/').split('/')[-1], str(int(time.time() * 1000))
            params = dict(build='16597', channel='8888', client_id='1089857299', country_code='CN', gnum=str(random.randint(10 ** 16, 10 ** 17 - 1)), id=vid, language='zh-Hans', local_time=timestamp, locale='1', model='iPhone17,2', network='wifi', os='26.5', play_type='2', resolution='1320*2868', session_id=''.join(random.choice('0123456789ABCDEF') for _ in range(32)), sigTime=timestamp, sigVersion='1.3', teenager_status='0', version='9.7.900', with_follow_chat_media='1')
            params['from'] = '48'; params['from_id'] = '1208'; params['sig'] = MeipaiVideoClient.getsig(params)
            api_url = 'https://api.meipai.com/medias/show.json?' + urllib.parse.urlencode(params)
            (resp := self.get(api_url, **request_overrides)).raise_for_status(); video_info.update(dict(raw_data=(raw_data := resp2json(resp=resp))))
            video_info.update(download_url=(lambda u: 'https:' + u if u.startswith('//') else u)(raw_data.get('video') or raw_data.get('dispatch_video') or ''))
            video_title = legalizestring((raw_data.get('caption') or raw_data.get('cover_title') or null_backup_title).strip(), replace_null_string=null_backup_title).removesuffix('.')
            guess_video_ext_result = FileTypeSniffer.getfileextensionfromurl(url=video_info.download_url, headers=self.default_download_headers, request_overrides=request_overrides, cookies=self.default_download_cookies)
            ext = guess_video_ext_result['ext'] if guess_video_ext_result['ext'] and guess_video_ext_result['ext'] != 'NULL' else 'mp4'
            video_info.update(dict(title=video_title, save_path=os.path.join(self.work_dir, self.source, f'{video_title}.{ext}'), ext=ext, guess_video_ext_result=guess_video_ext_result, identifier=vid, cover_url=raw_data.get('cover_pic') or raw_data.get('first_frame_pic')))
        except Exception as err:
            video_info.update(dict(err_msg=(err_msg := f'{self.source}.parsefromurl >>> {url} (Error: {err})')))
            self.logger_handle.error(err_msg, disable_print=self.disable_print)
        # return
        return [video_info]
    '''belongto'''
    @staticmethod
    def belongto(url: str, valid_domains: list[str] | set[str] = None):
        valid_domains = set(valid_domains or []) | {"meipai.com"}
        return BaseVideoClient.belongto(url, valid_domains)