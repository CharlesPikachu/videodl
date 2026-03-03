'''
Function:
    Implementation of HLS Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import re
import ssl
import time
import urllib
import requests
import statistics
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from collections import deque
from contextlib import suppress
from .misc import floatornone, intornone
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Sequence, Union, Literal, Optional, Dict, List, Tuple


'''settings'''
PickMode = Union[int, Literal["best"]]
BestStrategy = Literal["global_host", "per_segment"]
ProbeMethod = Literal["head_then_range_get", "range_get_only"]


'''writevodm3u8fortencent'''
def writevodm3u8fortencent(
        segments: Sequence[str], out_path: Union[str, Path], *, seg_duration: float = 10.0, pick: PickMode = 0, strategy: BestStrategy = "global_host", media_sequence: int = 1, playlist_type_vod: bool = True, strict: bool = True, probe_method: ProbeMethod = "head_then_range_get", 
        probe_timeout: float = 5.0, probe_workers: int = 16, samples_per_host: int = 2, range_bytes: int = 1024, default_headers: dict = None, default_cookies: dict = None, verbose: bool = False, request_overrides: dict = None,
    ) -> Path:
    # init
    default_headers, default_cookies, request_overrides = default_headers or {}, default_cookies or {}, request_overrides or {}
    out_path = Path(out_path); out_path.parent.mkdir(parents=True, exist_ok=True)
    host_func = lambda u: (urlparse(str(u)).netloc or "").lower()
    pickindex_func = lambda parts, idx: parts[idx] if 0 <= idx < len(parts) else parts[0]
    # parse candidates
    parsed: List[List[str]] = []
    for item in segments:
        if not item: continue
        line = str(item).strip()
        if not line: continue
        parts = [p.strip() for p in line.split("\t") if p.strip()]
        parts = [p.replace(" ", "") for p in parts if p.startswith(("http://", "https://"))]
        if parts: parsed.append(parts)
    if strict and not parsed: raise ValueError("no valid http(s) URLs found in `segments`.")
    ok_statuses = {200, 206, 301, 302, 303, 307, 308}
    # probe function definition
    def probeonce_func(url: str) -> Tuple[bool, float, Optional[int], Optional[str]]:
        def head_func() -> Tuple[bool, float, Optional[int], Optional[str]]:
            t0 = time.perf_counter()
            try: resp = requests.head(url, headers=default_headers, timeout=probe_timeout, allow_redirects=True, cookies=default_cookies, **request_overrides); elapsed = time.perf_counter() - t0; return (resp.status_code in ok_statuses, elapsed, resp.status_code, None)
            except requests.RequestException as err: elapsed = time.perf_counter() - t0; return (False, elapsed, None, f"{type(err).__name__}:{err}")
        def rangeget_func() -> Tuple[bool, float, Optional[int], Optional[str]]:
            t0 = time.perf_counter()
            headers = dict(default_headers)
            headers["Range"] = f"bytes=0-{max(0, range_bytes-1)}"
            try:
                resp = requests.get(url, headers=headers, timeout=probe_timeout, allow_redirects=True, stream=True, cookies=default_cookies, **request_overrides)
                with suppress(Exception): next(resp.iter_content(chunk_size=1), b"")
                elapsed = time.perf_counter() - t0; return (resp.status_code in ok_statuses, elapsed, resp.status_code, None)
            except requests.RequestException as err:
                elapsed = time.perf_counter() - t0
                return (False, elapsed, None, f"{type(err).__name__}:{err}")
        if probe_method == "range_get_only": return rangeget_func()
        ok, elapsed, code, err = head_func()
        if ok: return ok, elapsed, code, err
        return rangeget_func()
    # probe pick best function
    def probepickbest_func(parts: List[str]) -> str:
        best_u, best_t = None, float("inf")
        with ThreadPoolExecutor(max_workers=min(len(parts), max(1, probe_workers))) as ex:
            futs = {ex.submit(probeonce_func, u): u for u in parts}
            for fut in as_completed(futs):
                u = futs[fut]
                ok, elapsed, code, err = fut.result()
                if verbose: print(f"[probe seg] ok={ok} t={elapsed:.3f}s code={code} url={u} err={err}")
                if ok and elapsed < best_t: best_t, best_u = elapsed, u
        return best_u if best_u is not None else parts[0]
    # choose urls
    chosen_urls: List[str] = []
    # pick based on given arguments
    if pick != "best": idx = int(pick); chosen_urls = [pickindex_func(parts, idx) for parts in parsed]
    else:
        if strategy == "per_segment": chosen_urls = [probepickbest_func(parts) for parts in parsed]
        else:
            host_samples: Dict[str, List[str]] = {}
            deque(((h:=host_func(u)) and ((lst:=host_samples.setdefault(h, [])) is not None) and (len(lst) < samples_per_host) and (lst.append(u) or True) for parts in parsed for u in parts), maxlen=0)
            if strict and not host_samples: raise ValueError("pick='best': no hosts found to probe.")
            host_ok: Dict[str, int] = {h: 0 for h in host_samples}; host_lat: Dict[str, List[float]] = {h: [] for h in host_samples}
            with ThreadPoolExecutor(max_workers=max(1, probe_workers)) as ex:
                futs = []; deque((futs.append((h, u, ex.submit(probeonce_func, u))) for h, urls in host_samples.items() for u in urls), maxlen=0)
                for h, u, fut in futs:
                    ok, elapsed, code, err = fut.result()
                    if verbose: print(f"[probe host] {h} ok={ok} t={elapsed:.3f}s code={code} url={u} err={err}")
                    if ok: host_ok[h] += 1; host_lat[h].append(elapsed)
            scored = [(host_ok[h], statistics.median(host_lat[h]) if host_lat[h] else float("inf"), h) for h in host_samples if host_ok[h] > 0]
            if strict and not scored: raise ValueError("pick='best' (global_host): no reachable host found in probes.")
            scored.sort(key=lambda x: (-x[0], x[1], x[2])); best_host = scored[0][2]
            if verbose: print(f"[best_host] {best_host} ok_samples={scored[0][0]} median={scored[0][1]:.3f}s")
            for parts in parsed: u = next((x for x in parts if host_func(x) == best_host), None); chosen_urls.append(u if u is not None else probepickbest_func(parts))
    if strict and not chosen_urls: raise ValueError("no segments chosen (unexpected).")
    # write m3u8
    target_duration = int(seg_duration) if float(seg_duration).is_integer() else int(seg_duration) + 1
    lines: List[str] = ["#EXTM3U", "#EXT-X-VERSION:3", f"#EXT-X-TARGETDURATION:{target_duration}", f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}"]
    if playlist_type_vod: lines.append("#EXT-X-PLAYLIST-TYPE:VOD")
    for u in chosen_urls: lines.append(f"#EXTINF:{seg_duration:.3f},"); lines.append(u)
    lines.append("#EXT-X-ENDLIST")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # return
    return out_path


'''createsslcontext'''
def createsslcontext():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


'''naivedownloadwebpage'''
def naivedownloadwebpage(url, headers: dict = None, query: dict = None):
    if query: filtered_query = {k: v for k, v in query.items() if v is not None}; url = url + '?' + urllib.parse.urlencode(filtered_query)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    req.add_header('Accept-Language', 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    if headers: _ = tuple(req.add_header(k, v) for k, v in headers.items())
    ctx = createsslcontext()
    try: resp = urllib.request.urlopen(req, context=ctx, timeout=30)
    except urllib.error.HTTPError as e: raise Exception(f'HTTP Error {e.code}: {e.reason} for URL {url}')
    except urllib.error.URLError as e: raise Exception(f'URL Error: {e.reason} for URL {url}')
    data: bytes = resp.read()
    for encoding in ('utf-8', 'gbk', 'gb2312', 'latin-1'):
        try: return data.decode(encoding)
        except UnicodeDecodeError: continue
    return data.decode('utf-8', errors='replace')


'''naiveparsem3u8formats'''
def naiveparsem3u8formats(m3u8_url: str):
    formats, subtitles = [], {}
    try: m3u8_text: str = naivedownloadwebpage(m3u8_url)
    except Exception: return [{'url': m3u8_url, 'ext': 'mp4', 'protocol': 'm3u8'}], {}
    if '#EXTM3U' not in m3u8_text: return [{'url': m3u8_url, 'ext': 'mp4', 'protocol': 'm3u8'}], {}
    base_url = m3u8_url.rsplit('/', 1)[0] + '/'; lines = m3u8_text.strip().splitlines(); i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXT-X-STREAM-INF:'):
            attrs = naiveparsem3u8attributes(line[len('#EXT-X-STREAM-INF:'):]); i += 1
            if i < len(lines):
                stream_url = lines[i].strip()
                if not stream_url.startswith('http'): stream_url = urllib.parse.urljoin(base_url, stream_url)
                fmt = {'url': stream_url, 'ext': 'mp4', 'protocol': 'm3u8_native'}
                if 'BANDWIDTH' in attrs: fmt['tbr'] = floatornone(attrs['BANDWIDTH'], scale=1000)
                if 'RESOLUTION' in attrs: (res := attrs.get('RESOLUTION')) and ('x' in res) and (lambda w, h: fmt.update({'width': intornone(w), 'height': intornone(h)}))(*res.split('x', 1))
                formats.append(fmt)
        elif line.startswith('#EXT-X-MEDIA:') and 'TYPE=SUBTITLES' in line:
            attrs = naiveparsem3u8attributes(line[len('#EXT-X-MEDIA:'):]); sub_url: str = attrs.get('URI', '')
            if sub_url and not sub_url.startswith('http'): sub_url = urllib.parse.urljoin(base_url, sub_url)
            lang = attrs.get('LANGUAGE', attrs.get('NAME', 'und')).lower().strip('"')
            if sub_url: subtitles.setdefault(lang, []).append({'url': sub_url, 'ext': 'vtt'})
        i += 1
    if not formats: formats.append({'url': m3u8_url, 'ext': 'mp4', 'protocol': 'm3u8_native'})
    return formats, subtitles


'''naiveparsem3u8attributes'''
def naiveparsem3u8attributes(line):
    attrs = {}
    for m in re.finditer(r'([A-Z0-9-]+)=(?:"([^"]*?)"|([^,]*))', line): attrs[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
    return attrs


'''HLSBestParser'''
class HLSBestParser:
    KV = re.compile(r'([A-Z0-9\-]+)=(".*?"|[^,]*)')
    def __init__(self, master_url: str | None = None):
        self.master_url = master_url
    '''best'''
    def best(self, master_text: str) -> dict:
        lines, variants, idx = [ln.strip() for ln in master_text.splitlines() if ln.strip()], [], 0
        while idx < len(lines):
            line = lines[idx]
            if not line.startswith("#EXT-X-STREAM-INF:"): idx += 1; continue
            attrs_text = line.split(":", 1)[1]
            attrs = {k: str(v[1: -1] if str(v).startswith('"') and str(v).endswith('"') else v).strip() for k, v in self.KV.findall(attrs_text)}
            uri_idx = idx + 1
            while uri_idx < len(lines) and (lines[uri_idx].startswith("#") or not lines[uri_idx]): uri_idx += 1
            if uri_idx >= len(lines): break
            uri = urljoin(self.master_url, lines[uri_idx]) if self.master_url else lines[uri_idx]
            bandwidth = int(attrs.get("BANDWIDTH", "0") or 0)
            res = attrs.get("RESOLUTION", "")
            width, height = (map(int, res.lower().split("x", 1)) if "x" in res else (0, 0))
            variants.append({"uri": uri, "bandwidth": bandwidth, "resolution": (width, height), "attrs": attrs, "score": (width * height, bandwidth)})
            idx = uri_idx; idx += 1
        if not variants: raise ValueError("No HLS variants found")
        return max(variants, key=lambda v: v["score"])