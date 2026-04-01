'''
Function:
    Implementation of BrightcoveSmuggler
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import re
import html
import json
import copy
import requests
from .misc import resp2json
from urllib.parse import urlsplit, parse_qs, urljoin, urlencode


'''BrightcoveSmuggler'''
class BrightcoveSmuggler():
    '''smuggleurl'''
    @staticmethod
    def smuggleurl(url, data: dict):
        url, idata = BrightcoveSmuggler.unsmuggleurl(url, {}); data.update(idata)
        sdata = urlencode({'__videodl_smuggle': json.dumps(data)})
        return url + '#' + sdata
    '''unsmuggleurl'''
    @staticmethod
    def unsmuggleurl(smug_url: str, default=None):
        if '#__videodl_smuggle' not in smug_url: return smug_url, default
        url, _, sdata = smug_url.rpartition('#')
        data = json.loads(parse_qs(sdata)['__videodl_smuggle'][0])
        return url, data
    '''parse'''
    @staticmethod
    def extract(player_url, request_overrides: dict = None):
        request_overrides, session = copy.deepcopy(request_overrides or {}), requests.Session()
        account_id, player_id, video_id = BrightcoveSmuggler._parseplayerurl(player_url)
        policy_key = BrightcoveSmuggler._fetchpolicykey(session=session, player_url=player_url, request_overrides=request_overrides)
        api_url = f'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36', 'Accept': f'application/json;pk={policy_key}', 'BCOV-Policy': policy_key, 'Origin': 'https://players.brightcove.net', 'Referer': player_url}
        request_overrides.pop('headers', None); (resp := session.get(api_url, headers=headers, **request_overrides)).raise_for_status()
        data = resp2json(resp=resp); formats: list[dict] = []
        for s in data.get('sources', []):
            if (not isinstance(s, dict)) or (not (src := s.get('src'))): continue
            formats.append({'url': src, 'type': s.get('type'), 'container': s.get('container'), 'codec': s.get('codec') or s.get('codecs'), 'height': s.get('height'), 'width': s.get('width'), 'avg_bitrate': s.get('avg_bitrate') or s.get('bitrate')})
        formats.sort(key=lambda f: (f.get('height') or 0, f.get('avg_bitrate') or 0), reverse=True)
        return {'id': data.get('id') or video_id, 'title': data.get('name'), 'formats': formats, 'raw': data, 'player_url': player_url}
    '''_parseplayerurl'''
    @staticmethod
    def _parseplayerurl(player_url: str):
        m = re.search(r'players\.brightcove\.net/(\d+)/([^/]+)_default/index\.html', player_url)
        account_id, player_id, video_id = m.group(1), m.group(2), parse_qs(urlsplit(player_url).query).get('videoId', [None])[0]
        return account_id, player_id, video_id
    '''_extractpolicykeyfromhtml'''
    @staticmethod
    def _extractpolicykeyfromhtml(html_text: str):
        if (m := re.search(r'"policyKey"\s*:\s*"([^"]+)"', html_text)): return m.group(1)
        if (m := re.search(r'policyKey\s*:\s*"([^"]+)"', html_text)): return m.group(1)
        return None
    '''_fetchpolicykey'''
    @staticmethod
    def _fetchpolicykey(session: requests.Session, player_url: str, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        (resp := session.get(player_url, **request_overrides)).raise_for_status()
        if (policy_key := BrightcoveSmuggler._extractpolicykeyfromhtml(resp.text)): return policy_key
        m = re.search(r'<script[^>]+src="([^"]*index(?:\.min)?\.js[^"]*)"[^>]*>', resp.text, flags=re.IGNORECASE)
        (js_resp := session.get(urljoin(player_url, html.unescape(m.group(1))), **request_overrides)).raise_for_status()
        return BrightcoveSmuggler._extractpolicykeyfromhtml(js_resp.text)