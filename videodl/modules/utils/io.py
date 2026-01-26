'''
Function:
    Implementation of IO Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
import uuid
import pathlib
from pathvalidate import sanitize_filepath


'''touchdir'''
def touchdir(directory, exist_ok=True, mode=511, auto_sanitize=True):
    if auto_sanitize: directory = sanitize_filepath(directory)
    return os.makedirs(directory, exist_ok=exist_ok, mode=mode)


'''generateuniquetmppath'''
def generateuniquetmppath(dir: str = ".", ext: str = 'mp4'):
    d = pathlib.Path(dir)
    while True:
        p = d / f"{uuid.uuid4().hex}.{ext}"
        try:
            fd = os.open(p, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return str(p)
        except FileExistsError:
            pass