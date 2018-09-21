# 作者：Charles
# 公众号：Charles的皮卡丘
# 腾讯视频下载:
# 	-https://v.qq.com/
import os
import re
import sys
import json
import click
import urllib
import requests
from contextlib import closing
sys.path.append('..')
from utils.utils import *


'''
Input:
	-url: 视频地址
	-savepath: 视频下载后保存的路径
	-app: 在cmd窗口运行还是在Demo中调用该类
Output:
	-返回下载响应码
'''
class tecent():
	def __init__(self):
		self.headers = {
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
		# [fhd, shd, hd, sd]
		self.info_url = 'http://vv.video.qq.com/getinfo?otype=json&appver=3.2.19.335&platform={}&defnpayver=1&defn=shd&vid={}'
		self.key_url = 'http://vv.video.qq.com/getkey?otype=json&platform=11&format={}&vid={}&filename={}&appver=3.2.19.335'
	# 外部调用
	def get(self, url, savepath='./videos', app='demo'):
		Vurlinfos = self._getvideoinfos(url)
		res = None
		if app == 'cmd':
			for Vurlinfo in Vurlinfos:
				res = self._download_cmd(Vurlinfo, savepath)
		elif app == 'demo':
			for Vurlinfo in Vurlinfos:
				res = self._download_demo(Vurlinfo, savepath)
		return res
	# Demo用
	def _download_demo(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'tecent_' + Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_tms(download_url, name)
			return 200
		except:
			return 404
	# Cmd用
	def _download_cmd(self, Vurlinfos, savepath):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = 'tecent_' + Vurlinfos[1] + '.mp4'
		download_url = Vurlinfos[0]
		if not download_url:
			return 404
		try:
			download_tms(download_url, name)
			return 200
		except:
			return 404
	# 获得视频信息
	def _getvideoinfos(self, url):
		Vurlinfos = []
		platforms = [4100201, 11]
		vid = url.split('/')[-1].split('.')[0]
		if len(vid) != 11:
			res = requests.get(url, headers=self.headers)
			url = re.findall(r'rel="canonical".*?href="(.*?)"', res.text)[0]
			vid = url.split('/')[-1].split('.')[0]
		is_find = False
		for platform in platforms:
			res = requests.get(url=self.info_url.format(platform, vid), headers=self.headers)
			if len(re.findall(r'"url":(.*?),', res.text)) >= 1:
				is_find = True
			info_json = json.loads(re.findall(r'QZOutputJson=(.*)', res.text)[0][:-1])
			if is_find:
				break
		try:
			lnk = info_json['vl']['vi'][0]['lnk']
			title = info_json['vl']['vi'][0]['ti']
			url = info_json['vl']['vi'][0]['ul']['ui'][0]['url']
			fc = info_json['vl']['vi'][0]['cl']['fc']
			fn = info_json['vl']['vi'][0]['fn']
		except:
			return [None, None]
		assert fn.split('.')[0] == lnk
		constant, video_type = fn.split('.')[-2], fn.split('.')[-1]
		flag = True
		if fc == 0:
			fc = 1
			flag = False
		download_url = []
		for i in range(fc):
			if flag:
				keyid = info_json['vl']['vi'][0]['cl']['ci'][i]['keyid'].split('.')[1]
				fn = '.'.join([lnk, constant, str(i+1), video_type])
			else:
				keyid = info_json['vl']['vi'][0]['cl']['keyid'].split('.')[-1]
			res = requests.get(url=self.key_url.format(keyid, vid, fn), headers=self.headers)
			res_json = json.loads(re.findall(r'QZOutputJson=(.*)', res.text)[0][:-1])
			if not res_json.get('key'):
				try:
					key = res_json['v1']['vi'][0]['fvkey']
					download_url_part = '{}{}?vkey={}'.format(url, lnk+'.'+video_type, key)
				except:
					download_url_part = None
			else:
				key = res_json.get('key')
				download_url_part = '{}{}?vkey={}'.format(url, fn, key)
			download_url.append(download_url_part)
		Vname = title
		Vurlinfos.append([download_url, Vname])
		return Vurlinfos


# 测试用
if __name__ == '__main__':
	url = 'https://v.qq.com/x/cover/7r83y1oca851nq6/g07185bhudr.html'
	# tecent().get(url, savepath='./videos', app='demo')
	tecent().get(url, savepath='./videos', app='cmd')