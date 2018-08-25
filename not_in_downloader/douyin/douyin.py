# 作者: Charles
# 公众号: Charles的皮卡丘
# 抖音下载器V4.0
import os
import re
import json
import click
import random
import requests
from contextlib import closing
from ipaddress import ip_address
from subprocess import Popen, PIPE
import warnings
warnings.filterwarnings("ignore")


# 抖音视频下载类
# 视频下载后保存在抖音号对应的昵称名文件夹下
# 脚本运行需先安装nodejs: https://nodejs.org/
class douyin():
	def __init__(self):
		self.headers = {
						'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
						'cache-control': 'max-age=0',
						'accept-language': 'zh-CN,zh;q=0.9',
						'accept-encoding': 'gzip, deflate, br',
						'upgrade-insecure-requests': '1',
						'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
						'X-Real-IP': None,
						'X-Forwarded-For': None
						}
		while True:
			ip = ip_address('.'.join(map(str, (random.randint(0, 255) for _ in range(4)))))
			if ip.is_private:
				self.headers['X-Real-IP'], self.headers['X-Forwarded-For'] = str(ip), str(ip)
				break
		self.share_url = 'https://www.amemv.com/share/user/{}'
		self.user_url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id={}&max_cursor={}&count=21&aid=1128&_signature={}&dytk={}'
		print('[INFO]:Douyin App-Video downloader...')
		print('[Version]: V4.1')
		print('[Author]: Charles')
		print('[HELP]: Enter user id to download videos, Enter <q> to quit...')
	# 外部调用运行
	def run(self):
		user_id = input('Enter the userID:')
		if user_id == 'q' or user_id == 'Q':
			return None
		watermark = input('With watermark or not(0=Yes or 1=No):')
		if watermark == 'q' or watermark == 'Q':
			return None
		if watermark == '0':
			watermark = True
		else:
			watermark = False
		video_names, video_urls, nickname = self._get_urls_by_userid(user_id)
		if video_names is None:
			return None
		num_url = len(video_urls)
		print('[INFO]: Find %d videos...' % num_url)
		for i in range(num_url):
			print('[INFO]: Downloading No.%d video...' % i)
			video_name = video_names[i]
			video_url = video_urls[i]
			if not watermark:
				video_url = video_url.replace('playwm', 'play')
			# 避免重复下载
			if not os.path.isfile(os.path.join(nickname, video_name)):
				self._download([video_name, video_url], savepath=nickname)
		print('[INFO]: All done!')
		return user_id
	# 下载
	def _download(self, Vurlinfos, savepath='./videos'):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		name = Vurlinfos[0]
		download_url = Vurlinfos[1]
		with closing(requests.get(download_url, headers=self.headers, stream=True, verify=False)) as res:
			total_size = int(res.headers['content-length'])
			if res.status_code == 200:
				label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
				with click.progressbar(length=total_size, label=label) as progressbar:
					with open(os.path.join(savepath, name), "wb") as f:
						for chunk in res.iter_content(chunk_size=1024):
							if chunk:
								f.write(chunk)
								progressbar.update(1024)
			else:
				print('[ERROR]:Connect error...')
			return res.status_code
	# 根据抖音号获得账号所有视频下载地址
	def _get_urls_by_userid(self, user_id):
		uid = user_id
		try:
			process = Popen(['node', 'fuck-byted-acrawler.js', str(uid)], stdout=PIPE, stderr=PIPE)
		except:
			print('[Error]: Nodejs is needed...')
			exit(-1)
		signature = process.communicate()[0].decode().strip('\n')
		res = requests.get(self.share_url.format(uid), headers=self.headers)
		try:
			dytk = re.findall(r"dytk: '(.+)'", res.text)[0]
		except:
			print('[Error]: User Id error...')
			return None, None, None
		try:
			nickname = re.findall(r'"nickname"\>(.+?)\<', res.text)[0].replace(' ', '').replace('\\', '').replace('/', '')
		except:
			nickname = str(uid)
		max_cursor = 0
		video_names = []
		video_urls = []
		while True:
			res = requests.get(self.user_url.format(uid, max_cursor, signature, dytk), headers=self.headers)
			res_json = json.loads(res.text)
			for aweme in res_json['aweme_list']:
				aweme_id = aweme['aweme_id']
				video_url = aweme['video']['play_addr']['url_list'][0]
				video_names.append('aweme_id'+'_'+aweme_id+'.mp4')
				video_urls.append(video_url)
			max_cursor = res_json['max_cursor']
			if not res_json['has_more']:
				break
		return video_names, video_urls, nickname


if __name__ == '__main__':
	dy = douyin()
	while True:
		res = dy.run()
		if res is None:
			break