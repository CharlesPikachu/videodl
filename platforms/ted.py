'''
Function:
	TED演讲视频下载: https://www.ted.com/talks?language=zh-cn
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import json
import requests
from utils.utils import *
requests.packages.urllib3.disable_warnings()


'''
Input:
	--url: 视频地址
	--savepath: 视频下载后保存的路径
Output:
	--is_success: 下载是否成功的BOOL值
'''
class ted():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
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
		video_name = 'ted_' + video_infos[1] + '.mp4'
		try:
			is_success = downloadBASE(url=download_url, savename=video_name, savepath=savepath, headers=self.headers, stream=True, verify=False)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		res = requests.get(url, headers=self.headers)
		temp = '{' + re.findall(r'"__INITIAL_DATA__"\s*:\s*\{(.+)\}', res.text)[0]
		temp_json = json.loads(temp)
		title = temp_json['talks'][0]['title']
		if not title:
			title = 'vid' + str(temp_json['talks'][0]['downloads']['id'])
		videos_dict = temp_json['talks'][0]['downloads']['nativeDownloads']
		# 选择质量最好的视频下载
		for quality in ['high', 'medium', 'low']:
			if quality in videos_dict:
				download_url = videos_dict[quality]
				break
		video_infos = [download_url, title]
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'https://www.ted.com/talks/glenn_cantave_how_augmented_reality_is_changing_activism?language=zh-tw'
	ted().get(url, savepath='videos')