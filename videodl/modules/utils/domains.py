'''
Function:
    Implementation of Domain Related Function
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from functools import lru_cache
from urllib.parse import urlsplit


'''settings'''
YOUKU_SUFFIXES = {"youku.com", "youku.tv", "tudou.com", "laifeng.com", "soku.com", "paike.com"}
IQIYI_SUFFIXES = {"iqiyi.com", "qiyi.com", "iq.com", "pps.tv", "ppstream.com"}
TENCENT_SUFFIXES = {"v.qq.com", "film.qq.com", "wetv.vip", "wetv.qq.com"}
MANGO_SUFFIXES = {"mgtv.com", "hunantv.com", "imgo.tv"}
PPTV_SUFFIXES = {"pptv.com", "pplive.com"}
CCTV_SUFFIXES = {"cctv.com", "cctv.cn", "cntv.cn"}
BILIBILI_SUFFIXES = {"bilibili.com", "b23.tv", "bilibili.tv"}


'''obtainhostname'''
@lru_cache(maxsize=200_000)
def obtainhostname(url: str) -> str | None:
    if not url: return None
    u = url.strip()
    if "://" not in u: u = "https://" + u
    try: host = urlsplit(u).hostname
    except Exception: return None
    return host.lower().strip(".") if host else None


'''hostmatchessuffix'''
def hostmatchessuffix(host: str | None, suffixes: set[str]) -> bool:
    if not host: return False
    h = host.lower().strip(".")
    for s in suffixes:
        s = s.lower().strip(".")
        if h == s or h.endswith("." + s): return True
    return False