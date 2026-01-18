'''
Function:
    Implementation of HLS Related Functions
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import re
import time
import requests
import statistics
from pathlib import Path
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Sequence, Union, Literal, Optional, Dict, List, Tuple


'''settings'''
PickMode = Union[int, Literal["best"]]
BestStrategy = Literal["global_host", "per_segment"]
ProbeMethod = Literal["head_then_range_get", "range_get_only"]


'''writevodm3u8fortencent'''
def writevodm3u8fortencent(
        segments: Sequence[str], out_path: Union[str, Path], *, seg_duration: float = 10.0, pick: PickMode = 0, strategy: BestStrategy = "global_host",
        media_sequence: int = 1, playlist_type_vod: bool = True, strict: bool = True, probe_method: ProbeMethod = "head_then_range_get", probe_timeout: float = 5.0,
        probe_workers: int = 16, samples_per_host: int = 2, range_bytes: int = 1024, default_headers: dict = None, default_cookies: dict = None, verbose: bool = False,
        request_overrides: dict = None,
    ) -> Path:
    # init
    default_headers, default_cookies, request_overrides = default_headers or {}, default_cookies or {}, request_overrides or {}
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    def _host(u: str) -> str:
        return (urlparse(u).netloc or "").lower()
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
    def _probeonce(url: str) -> Tuple[bool, float, Optional[int], Optional[str]]:
        def _head() -> Tuple[bool, float, Optional[int], Optional[str]]:
            t0 = time.perf_counter()
            try:
                resp = requests.head(url, headers=default_headers, timeout=probe_timeout, allow_redirects=True, cookies=default_cookies, **request_overrides)
                elapsed = time.perf_counter() - t0
                return (resp.status_code in ok_statuses, elapsed, resp.status_code, None)
            except requests.RequestException as err:
                elapsed = time.perf_counter() - t0
                return (False, elapsed, None, f"{type(err).__name__}:{err}")
        def _rangeget() -> Tuple[bool, float, Optional[int], Optional[str]]:
            t0 = time.perf_counter()
            headers = dict(default_headers)
            headers["Range"] = f"bytes=0-{max(0, range_bytes-1)}"
            try:
                resp = requests.get(url, headers=headers, timeout=probe_timeout, allow_redirects=True, stream=True, cookies=default_cookies, **request_overrides)
                try:
                    _ = next(resp.iter_content(chunk_size=1), b"")
                except Exception:
                    pass
                elapsed = time.perf_counter() - t0
                return (resp.status_code in ok_statuses, elapsed, resp.status_code, None)
            except requests.RequestException as err:
                elapsed = time.perf_counter() - t0
                return (False, elapsed, None, f"{type(err).__name__}:{err}")
        if probe_method == "range_get_only": return _rangeget()
        ok, elapsed, code, err = _head()
        if ok: return ok, elapsed, code, err
        return _rangeget()
    # pick index function
    def _pickindex(parts: List[str], idx: int) -> str:
        return parts[idx] if 0 <= idx < len(parts) else parts[0]
    # probe pick best function
    def _probepickbest(parts: List[str]) -> str:
        best_u, best_t = None, float("inf")
        with ThreadPoolExecutor(max_workers=min(len(parts), max(1, probe_workers))) as ex:
            futs = {ex.submit(_probeonce, u): u for u in parts}
            for fut in as_completed(futs):
                u = futs[fut]
                ok, elapsed, code, err = fut.result()
                if verbose:
                    print(f"[probe seg] ok={ok} t={elapsed:.3f}s code={code} url={u} err={err}")
                if ok and elapsed < best_t:
                    best_t, best_u = elapsed, u
        return best_u if best_u is not None else parts[0]
    # choose urls
    chosen_urls: List[str] = []
    # pick based on given arguments
    if pick != "best":
        idx = int(pick)
        chosen_urls = [_pickindex(parts, idx) for parts in parsed]
    else:
        if strategy == "per_segment":
            chosen_urls = [_probepickbest(parts) for parts in parsed]
        else:
            host_samples: Dict[str, List[str]] = {}
            for parts in parsed:
                for u in parts:
                    h = _host(u)
                    if not h: continue
                    lst = host_samples.setdefault(h, [])
                    if len(lst) < samples_per_host: lst.append(u)
            if strict and not host_samples: raise ValueError("pick='best': no hosts found to probe.")
            host_ok: Dict[str, int] = {h: 0 for h in host_samples}
            host_lat: Dict[str, List[float]] = {h: [] for h in host_samples}
            with ThreadPoolExecutor(max_workers=max(1, probe_workers)) as ex:
                futs = []
                for h, urls in host_samples.items():
                    for u in urls: futs.append((h, u, ex.submit(_probeonce, u)))
                for h, u, fut in futs:
                    ok, elapsed, code, err = fut.result()
                    if verbose: print(f"[probe host] {h} ok={ok} t={elapsed:.3f}s code={code} url={u} err={err}")
                    if ok: host_ok[h] += 1; host_lat[h].append(elapsed)
            scored = []
            for h in host_samples:
                if host_ok[h] <= 0: continue
                med = statistics.median(host_lat[h]) if host_lat[h] else float("inf")
                scored.append((host_ok[h], med, h))
            if strict and not scored: raise ValueError("pick='best' (global_host): no reachable host found in probes.")
            scored.sort(key=lambda x: (-x[0], x[1], x[2]))
            best_host = scored[0][2]
            if verbose: print(f"[best_host] {best_host} ok_samples={scored[0][0]} median={scored[0][1]:.3f}s")
            for parts in parsed:
                u = next((x for x in parts if _host(x) == best_host), None)
                chosen_urls.append(u if u is not None else _probepickbest(parts))
    if strict and not chosen_urls: raise ValueError("no segments chosen (unexpected).")
    # write m3u8
    target_duration = int(seg_duration) if float(seg_duration).is_integer() else int(seg_duration) + 1
    lines: List[str] = [
        "#EXTM3U", "#EXT-X-VERSION:3", f"#EXT-X-TARGETDURATION:{target_duration}", f"#EXT-X-MEDIA-SEQUENCE:{media_sequence}",
    ]
    if playlist_type_vod: lines.append("#EXT-X-PLAYLIST-TYPE:VOD")
    for u in chosen_urls:
        lines.append(f"#EXTINF:{seg_duration:.3f},")
        lines.append(u)
    lines.append("#EXT-X-ENDLIST")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # return
    return out_path


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
            if line.startswith("#EXT-X-STREAM-INF:"):
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
                idx = uri_idx
            idx += 1
        if not variants: raise ValueError("No HLS variants found")
        return max(variants, key=lambda v: v["score"])