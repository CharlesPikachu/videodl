'''
Function:
    Implementation of removepycache
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from __future__ import annotations
import os
import shutil
from pathlib import Path


'''removepycache'''
def removepycache(root: str | os.PathLike = ".") -> int:
    root_path, removed = Path(root).resolve(), 0
    for p in root_path.rglob("__pycache__"):
        if p.is_dir():
            try:
                shutil.rmtree(p)
                removed += 1
                print(f"Removed: {p}")
            except Exception as e:
                print(f"Failed:  {p}  ({e})")
    print(f"\nDone. Removed {removed} __pycache__ directories under {root_path}")
    return removed


'''run'''
if __name__ == "__main__":
    removepycache(".")