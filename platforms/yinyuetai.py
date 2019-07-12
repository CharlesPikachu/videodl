'''
Function:
	音悦台MV下载: http://www.yinyuetai.com
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import re
import requests
from utils.utils import *


'''
Input:
	--url: 视频地址
	--savepath: 视频下载后保存的路径
Output:
	--is_success: 下载是否成功的BOOL值
'''
class yinyuetai():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
					}
		self.info_url = 'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId={}'
	'''外部调用'''
	def get(self, url, savepath='videos'):
		video_infos = self.__getvideoinfos(url)
		is_success = self.__download(video_infos, savepath)
		return is_success
	'''下载'''
	def __download(self, video_infos, savepath):
		checkFolder(savepath)
		download_url = video_infos[0]
		video_name = 'yinyuetai_' + video_infos[1] + '.mp4'
		try:
			is_success = downloadBASE(url=download_url, savename=video_name, savepath=savepath, headers=self.headers, stream=True, verify=False)
		except:
			is_success = False
		return is_success
	'''获得视频信息'''
	def __getvideoinfos(self, url):
		mvid = url.split('/')[-1]
		res = requests.get(self.info_url.format(mvid), headers=self.headers)
		pattern = re.compile(r'http://\w*?\.yinyuetai\.com/uploads/videos/common/.*?(?=&br)')
		re_result = re.findall(pattern, res.text)
		# 选择质量最佳的视频
		download_url = re_result[-1]
		video_infos = [download_url, mvid]
		return video_infos


'''test'''
if __name__ == '__main__':
	url = 'http://v.yinyuetai.com/video/3247548'
	yinyuetai().get(url, savepath='videos')