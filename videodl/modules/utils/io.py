'''
Function:
    Implementation of IO Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import time
import uuid
import pathlib
from pathlib import Path
from pathvalidate import sanitize_filepath
fcntl = __import__("fcntl") if os.name != "nt" else None
msvcrt = __import__("msvcrt") if os.name == "nt" else None


'''safeunlinkpathobj'''
def safeunlinkpathobj(path: Path, max_retries=20, delay=0.1):
    for _ in range(max_retries):
        try: path.unlink(missing_ok=True); return True
        except Exception: time.sleep(delay)
    return False


'''touchdir'''
def touchdir(directory, exist_ok: bool = True, mode: int = 511, auto_sanitize: bool = True):
    if auto_sanitize: directory = sanitize_filepath(directory)
    return os.makedirs(directory, exist_ok=exist_ok, mode=mode)


'''generateuniquetmppath'''
def generateuniquetmppath(dir: str = ".", ext: str = 'mp4'):
    d = pathlib.Path(dir)
    while True:
        p = d / f"{uuid.uuid4().hex}.{ext}"
        try: fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.close(fd); return str(p)
        except FileExistsError: pass


'''FileLock'''
class FileLock:
    def __init__(self, lock_path: Path, timeout: float = 300.0, poll_interval: float = 0.2):
        self.fp = None
        self.timeout = timeout
        self.lock_path = Path(lock_path)
        self.poll_interval = poll_interval
    '''enter'''
    def __enter__(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self.fp = open(self.lock_path, "a+b"); self.fp.seek(0, os.SEEK_END)
        if self.fp.tell() == 0: self.fp.write(b"\0"); self.fp.flush()
        deadline = time.time() + self.timeout
        while True:
            try:
                if os.name == "nt": self.fp.seek(0); msvcrt.locking(self.fp.fileno(), msvcrt.LK_NBLCK, 1)
                else: fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except OSError:
                if time.time() >= deadline: raise TimeoutError(f"Timeout acquiring lock: {self.lock_path}")
                time.sleep(self.poll_interval)
    '''exit'''
    def __exit__(self, exc_type, exc, tb):
        try:
            if not self.fp: return
            if os.name == "nt": self.fp.seek(0); msvcrt.locking(self.fp.fileno(), msvcrt.LK_UNLCK, 1)
            else: fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
        finally:
            if self.fp: self.fp.close(); self.fp = None