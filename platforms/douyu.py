'''
Function:
	斗鱼视频下载: https://www.douyu.com/
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
class douyu():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						'cookie': 'dy_did=f4b3c1c49228dc8806fb2dd600081501;'
						}
		self.info_url = 'http://vmobile.douyu.com/video/getInfo?vid={}'
	'''外部调用'''
	def get(self, url, savepath='videos'):
		video_infos = self.__getvideoinfos(url)
		is_success = self.__download(video_infos, savepath)
		return is_success
	'''下载'''
	def __download(self, video_infos, savepath):
		checkFolder(savepath)
		download_url = video_infos[0]
		video_name = 'douyu_' + video_infos[1] + '.mp4'
		try:
			is_success = downloadM3U8(video_url=download_url, savename=video_name, savepath=savepath)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		vid = url.split('/')[-1]
		res = requests.get(url, headers=self.headers)
		title = re.findall(r'<h1>(.+?)</h1>', res.text)[0]
		if not title:
			title = vid
		res = requests.get(self.info_url.format(vid), headers=self.headers)
		res_json = json.loads(res.text)
		if res_json['error'] != 0:
			download_url = ''
		else:
			download_url = res_json['data']['video_url']
		video_infos = [download_url, title]
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'https://v.douyu.com/show/8KxjMdB3GQQvVLwb'
	douyu().get(url, savepath='videos')