# 作者：Charles
# 公众号：Charles的皮卡丘
# B站视频下载:
# 	-https://www.bilibili.com/
import os
import re
import sys
import json
import time
import click
import urllib
import requests
sys.path.append('..')
from utils.utils import *
from contextlib import closing


'''
Input:
	-url: 视频地址
	-savepath: 视频下载后保存的路径
	-app: 在cmd窗口运行还是在Demo中调用该类
Output:
	-返回下载响应码
'''
class bilibili():
	def __init__(self):
		self.infoheaders = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'accept-encoding': 'gzip, deflate, br',
						'accept-language': 'zh-CN,zh;q=0.9',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
					}
		self.downheaders = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'accept': '*/*',
						'accept-encoding': 'gzip, deflate, br',
						'accept-language': 'zh-CN,zh;q=0.9',
						'Referer': 'https://search.bilibili.com/all?keyword='
					}
	# 外部调用
	def get(self, url, savepath='./videos', app='demo'):
		Vurlinfos = self._getvideoinfos(url)
		res = None
		if app == 'cmd':
			res = self._download_cmd(Vurlinfos, savepath)
		elif app == 'demo':
			res = self._download_demo(Vurlinfos, savepath)
		return res
	# Demo用
	def _download_demo(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'bili_' + Vurlinfos[1] + '.flv'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_tms(download_url, name, savepath='./videos', headers=self.downheaders)
			return 200
		except:
			return 404
	# Cmd用
	def _download_cmd(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'bili_' + Vurlinfos[1] + '.flv'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_tms(download_url, name, savepath='./videos', headers=self.downheaders)
			return 200
		except:
			return 404
	# 获得视频信息
	def _getvideoinfos(self, url):
		qualities = {'1080P': 80, '720P': 48, '480P': 32, '360P': 16}
		res = requests.get(url=url, headers=self.infoheaders)
		try:
			title = re.findall(r'\<h1 title="(.*?)"\>', res.text)[20]
		except:
			title = str(time.time()).split('.')[0]
		pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
		re_result = re.findall(pattern, res.text)[0]
		temp = json.loads(re_result)
		download_url = []
		for d in temp['durl']:
			download_url.append(d['url'])
		Vurlinfos = [download_url, title]
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'https://www.bilibili.com/video/av6142859/?p=2'
	# bilibili().get(url, savepath='./videos', app='demo')
	bilibili().get(url, savepath='./videos', app='cmd')