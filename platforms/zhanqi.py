'''
Function:
	战旗TV视频下载: https://videos.zhanqi.tv/
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
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
class zhanqi():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
						}
		self.info_url = 'https://www.zhanqi.tv/api/static/v2.2/video/{}.json'
	'''外部调用'''
	def get(self, url, savepath='./videos', app='demo'):
		video_infos = self.__getvideoinfos(url)
		is_success = self.__download(video_infos, savepath)
		return is_success
	'''下载'''
	def __download(self, video_infos, savepath):
		checkFolder(savepath)
		video_name = 'zhanqi_' + video_infos[1] + '.mp4'
		download_url = video_infos[0]
		try:
			is_success = downloadM3U8(video_url=download_url, savename=video_name, savepath=savepath)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		vid = url.split('/')[-1].split('.')[0]
		res = requests.get(self.info_url.format(vid), headers=self.headers)
		res_json = json.loads(res.text)
		try:
			title = res_json['data']['title'].replace('\\', '').replace('/', '').replace('.', '')
			if not title:
				raise ValueError('title is None...')
		except:
			title = vid
		try:
			download_url = res_json['data']['playUrl']
		except:
			download_url = ''
		video_infos = [download_url, title]
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'https://www.zhanqi.tv/v2/videos/767817.html'
	zhanqi().get(url, savepath='videos')