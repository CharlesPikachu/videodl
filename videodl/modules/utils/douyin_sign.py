'''
Function:
    抖音 a_bogus 签名（供 DouyinVideoClient 调用 web 接口用）。

    抖音 web 接口（如 /aweme/v1/web/aweme/detail/）需要 a_bogus 反爬签名；该签名
    由前端 JS 算法生成、随抖音版本变化。这里复用 videodl 已自带的 node（nodejs_wheel）
    去跑 modules/js/douyin/sign.js（内置浏览器环境 polyfill + 按版本存放的算法文件
    a_bogus.<version>.js），匿名即可，不需要登录。

    要随抖音版本更新签名：在 modules/js/douyin/ 放新的 a_bogus.<新版本>.js，并设
    环境变量 ABOGUS_VERSION=<新版本>（或改 sign.js 里的 DEFAULT_VERSION）。
Author:
    Zhenchao Jin
'''
import os
import time
import random
import shutil
import subprocess
from pathlib import Path


'''sign.js 路径'''
_SIGN_JS = Path(__file__).resolve().parents[1] / 'js' / 'douyin' / 'sign.js'
'''默认桌面 UA（签名与请求必须用同一个 UA）'''
DEFAULT_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'


'''_node_bin: 解析可用的 node 可执行（优先 PATH，其次 nodejs_wheel 自带）'''
def _node_bin():
    if os.environ.get('DOUYIN_NODE_BIN'):
        return os.environ['DOUYIN_NODE_BIN']
    if shutil.which('node'):
        return 'node'
    try:
        from nodejs_wheel.executable import node_path  # type: ignore
        return str(node_path())
    except Exception:
        try:
            import nodejs_wheel
            cand = Path(nodejs_wheel.__file__).parent / ('node.exe' if os.name == 'nt' else 'node')
            if cand.exists():
                return str(cand)
        except Exception:
            pass
    return 'node'


'''get_a_bogus: 对查询串算 a_bogus，返回签名字符串'''
def get_a_bogus(query: str, user_agent: str = DEFAULT_UA, post_data: str = '', timeout: int = 20) -> str:
    cmd = [_node_bin(), str(_SIGN_JS), query, post_data, user_agent or DEFAULT_UA]
    out = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=timeout)
    if out.returncode != 0:
        raise RuntimeError(f'douyin a_bogus sign failed: {(out.stderr or "").strip()[:200]}')
    ab = (out.stdout or '').strip()
    if not ab:
        raise RuntimeError('douyin a_bogus sign returned empty')
    return ab


'''sign_query: 给一段查询串补上 &a_bogus=<签名>，返回可直接拼到 URL 的完整查询串'''
def sign_query(query: str, user_agent: str = DEFAULT_UA) -> str:
    from urllib.parse import quote
    ab = get_a_bogus(query, user_agent=user_agent)
    return f'{query}&a_bogus={quote(ab, safe="")}'


'''gen_verify_fp: 本地生成 verifyFp / s_v_web_id（格式 verify_<base36时间戳>_<36位uuid>）'''
def gen_verify_fp() -> str:
    base_str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ms = int(round(time.time() * 1000)); b36 = ''
    while ms > 0:
        r = ms % 36
        b36 = (str(r) if r < 10 else chr(ord('a') + r - 10)) + b36
        ms //= 36
    o = [''] * 36
    o[8] = o[13] = o[18] = o[23] = '_'; o[14] = '4'
    for i in range(36):
        if not o[i]:
            n = int(random.random() * 62)
            if i == 19:
                n = (3 & n) | 8
            o[i] = base_str[n]
    return f'verify_{b36}_{"".join(o)}'
