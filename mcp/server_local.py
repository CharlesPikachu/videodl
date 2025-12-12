'''
Function:
    Implementation of Naive MCP Examples
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import sys, logging
from mcp.server.fastmcp import FastMCP
from videodl import videodl as videodl_pkg


'''settings'''
_client = None
mcp = FastMCP("videodl")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def getclient(allowed_video_sources=None, init_video_clients_cfg=None, clients_threadings=None, requests_overrides=None, apply_common_video_clients_only=False):
    """get video client"""
    global _client
    if _client is None:
        init_video_clients_cfg = init_video_clients_cfg or {}
        for k in (allowed_video_sources or []):
            init_video_clients_cfg.setdefault(k, {})
            init_video_clients_cfg[k].setdefault("disable_print", True)
        _client = videodl_pkg.VideoClient(
            allowed_video_sources=allowed_video_sources or [], init_video_clients_cfg=init_video_clients_cfg, clients_threadings=clients_threadings or {},
            requests_overrides=requests_overrides or {}, apply_common_video_clients_only=apply_common_video_clients_only,
        )
    return _client


@mcp.tool()
def parsefromurl(url: str, allowed_video_sources: list[str] | None = None) -> dict:
    """Parse video infos from URL."""
    infos = getclient(allowed_video_sources=allowed_video_sources).parsefromurl(url=url)
    return {"video_infos": infos}


@mcp.tool()
def download(video_infos: list[dict]) -> dict:
    """Download videos described by video_infos."""
    getclient().download(video_infos=video_infos)
    return {"ok": True}


'''main'''
if __name__ == "__main__":
    mcp.run(transport="stdio")