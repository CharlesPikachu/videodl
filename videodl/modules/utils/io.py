'''
Function:
    Implementation of IO related operations
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import os
from pathvalidate import sanitize_filepath


'''touchdir'''
def touchdir(directory, exist_ok=True, mode=511, auto_sanitize=True):
    if auto_sanitize: directory = sanitize_filepath(directory)
    return os.makedirs(directory, exist_ok=exist_ok, mode=mode)