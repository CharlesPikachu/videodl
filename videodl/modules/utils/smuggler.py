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
import requests
from .misc import resp2json
from urllib.parse import urlsplit, parse_qs, urljoin, urlencode


'''BrightcoveSmuggler'''
class BrightcoveSmuggler():
    '''smuggleurl'''
    @staticmethod
    def smuggleurl(url, data: dict):
        url, idata = BrightcoveSmuggler.unsmuggleurl(url, {})
        data.update(idata)
        sdata = urlencode({'__videodl_smuggle': json.dumps(data)})
        return url + '#' + sdata
    '''unsmuggleurl'''
    @staticmethod
    def unsmuggleurl(smug_url: str, default=None):
        if '#__videodl_smuggle' not in smug_url: return smug_url, default
        url, _, sdata = smug_url.rpartition('#')
        jsond = parse_qs(sdata)['__videodl_smuggle'][0]
        data = json.loads(jsond)
        return url, data
    '''parse'''
    @staticmethod
    def extract(player_url, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        session = requests.Session()
        account_id, player_id, video_id = BrightcoveSmuggler._parseplayerurl(player_url)
        policy_key = BrightcoveSmuggler._fetchpolicykey(session=session, player_url=player_url, request_overrides=request_overrides)
        api_url = f'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept': f'application/json;pk={policy_key}',
            'BCOV-Policy': policy_key,
            'Origin': 'https://players.brightcove.net',
            'Referer': player_url,
        }
        request_overrides.pop('headers')
        resp = session.get(api_url, headers=headers, **request_overrides)
        resp.raise_for_status()
        data = resp2json(resp=resp)
        formats = []
        for s in data.get('sources', []):
            src = s.get('src')
            if not src: continue
            fmt = {
                'url': src, 'type': s.get('type'), 'container': s.get('container'), 'codec': s.get('codec') or s.get('codecs'), 'height': s.get('height'),
                'width': s.get('width'), 'avg_bitrate': s.get('avg_bitrate') or s.get('bitrate'),
            }
            formats.append(fmt)
        formats.sort(key=lambda f: (f.get('height') or 0, f.get('avg_bitrate') or 0), reverse=True)
        return {'id': data.get('id') or video_id, 'title': data.get('name'), 'formats': formats, 'raw': data, 'player_url': player_url}
    '''_parseplayerurl'''
    @staticmethod
    def _parseplayerurl(player_url: str):
        m = re.search(r'players\.brightcove\.net/(\d+)/([^/]+)_default/index\.html', player_url)
        account_id, player_id = m.group(1), m.group(2)
        qs = parse_qs(urlsplit(player_url).query)
        video_id = qs.get('videoId', [None])[0]
        return account_id, player_id, video_id
    '''_extractpolicykeyfromhtml'''
    @staticmethod
    def _extractpolicykeyfromhtml(html_text: str):
        m = re.search(r'"policyKey"\s*:\s*"([^"]+)"', html_text)
        if m: return m.group(1)
        m = re.search(r'policyKey\s*:\s*"([^"]+)"', html_text)
        if m: return m.group(1)
        return None
    '''_fetchpolicykey'''
    @staticmethod
    def _fetchpolicykey(session: requests.Session, player_url: str, request_overrides: dict = None):
        request_overrides = request_overrides or {}
        resp = session.get(player_url, **request_overrides)
        resp.raise_for_status()
        html_text = resp.text
        policy_key = BrightcoveSmuggler._extractpolicykeyfromhtml(html_text)
        if policy_key: return policy_key
        m = re.search(r'<script[^>]+src="([^"]*index(?:\.min)?\.js[^"]*)"[^>]*>', html_text, flags=re.IGNORECASE)
        js_url = urljoin(player_url, html.unescape(m.group(1)))
        js_resp = session.get(js_url, **request_overrides)
        js_resp.raise_for_status()
        policy_key = BrightcoveSmuggler._extractpolicykeyfromhtml(js_resp.text)
        return policy_key