'''
Function:
	CNTV视频下载: http://tv.cntv.cn/
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import json
import requests
from utils.utils import *


'''
Input:
	--url: 视频地址
	--savepath: 视频下载后保存的路径
Output:
	--is_success: 下载是否成功的BOOL值
'''
class cntv():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
		self.info_url = 'http://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={}'
	'''外部调用'''
	def get(self, url, savepath='videos'):
		video_infos = self.__getvideoinfos(url)
		is_success = self.__download(video_infos, savepath)
		return is_success
	'''下载'''
	def __download(self, video_infos, savepath):
		checkFolder(savepath)
		download_url = video_infos[0]
		video_name = 'cntv_' + video_infos[1] + '.mp4'
		try:
			is_success = downloadTMS(video_urls=download_url, savename=video_name, savepath=savepath)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		pid = url.split('/')[-1]
		res = requests.get(self.info_url.format(pid), headers=self.headers)
		res_json = json.loads(res.text)
		if res_json['ack'] == 'yes':
			title = res_json['title'].replace('\\', '').replace('/', '')
			videos_choice = res_json['video']
			# 选质量最好的下
			for quality in ['chapters4', 'chapters3', 'chapters2', 'chapters', 'lowChapters']:
				if quality in videos_choice:
					quality_infos = videos_choice.get(quality)
					download_url = []
					for qi in quality_infos:
						download_part = qi.get('url')
						if download_part:
							download_url.append(download_part)
					break
		else:
			title = ''
			download_url = ''
		video_infos = [download_url, title]
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'http://tv.cntv.cn/video/C10881/4ec8c6c1bdd941b0b11280769b036e8b'
	cntv().get(url, savepath='videos')