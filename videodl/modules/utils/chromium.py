'''
Function:
    Implementation of Chromium Related Utils
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
import sys
import subprocess


'''ensureplaywrightchromium'''
def ensureplaywrightchromium():
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)