'''
Function:
	B站视频下载: https://www.bilibili.com/
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import json
import time
import requests
from utils.utils import *


'''
Input:
	--url: 视频地址
	--savepath: 视频下载后保存的路径
Output:
	--is_success: 下载是否成功的BOOL值
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
	'''外部调用'''
	def get(self, url, savepath='videos'):
		video_infos = self.__getvideoinfos(url)
		is_success = self.__download(video_infos, savepath)
		return is_success
	'''下载'''
	def __download(self, video_infos, savepath):
		checkFolder(savepath)
		download_url = video_infos[0]
		video_name = 'bilibili_' + video_infos[1] + '.flv'
		is_success = downloadTMS(video_urls=download_url, savename=video_name, savepath=savepath)
		try:
			is_success = downloadTMS(video_urls=download_url, savename=video_name, savepath=savepath, headers=self.downheaders)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		qualities = {'1080P': 80, '720P': 64, '480P': 32, '360P': 16}
		res = requests.get(url=url, headers=self.infoheaders)
		try:
			title = re.findall(r'\<title data-vue-meta="true"\>(.*?)\</title\>', res.text)[0].replace('-bilibili', '').replace('_哔哩哔哩 (゜-゜)つロ 干杯~', '')
		except:
			title = str(time.time()).split('.')[0]
		pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
		re_result = re.findall(pattern, res.text)[0]
		temp = json.loads(re_result)
		download_url = []
		for d in temp['data']['durl']:
			download_url.append(d['url'])
		video_infos = [download_url, title]
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'https://www.bilibili.com/video/av6142859/?p=2'
	bilibili().get(url, savepath='videos')