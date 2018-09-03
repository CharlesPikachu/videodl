# 作者: Charles
# 公众号: Charles的皮卡丘
# 斗鱼直播缓存
# 代码仅供学习交流，禁止用于其他
import os
import time
import json
import hashlib
import requests


# 斗鱼直播缓存
class douyuTV():
	def __init__(self):
		self.api = "http://www.douyutv.com/api/v1/"
		self.headers = {
							'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/576.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/576.1.4'
						}
	# 缓存函数
	def cache(self, roomid, savepath='./Cache'):
		if not os.path.exists(savepath):
			os.mkdir(savepath)
		args = "room/%s?aid=wp&client_sys=wp&time=%d" % (roomid, int(time.time()))
		args_utf = (args + "zNzMV1y4EMxOHS6I5WKm").encode("utf-8")
		args_md5 = hashlib.md5(args_utf).hexdigest()
		url = "%s%s&auth=%s" % (self.api, args, args_md5)
		res = requests.get(url, headers=self.headers)
		res_json = json.loads(res.text)
		if res_json.get('error') != 0:
			print('[Error]: Fail to cache because of error %s...' % res_json.get('error'))
			return None
		data = res_json['data']
		room_name = data['room_name'].replace('\\', '').replace('//', '')
		if data.get('show_status') != '1':
			print('[Error]: Rome <%s> is not online...' % roomid)
		live_url = '%s/%s' % (data.get('rtmp_url'), data.get('rtmp_live'))
		savename = roomid + '.flv'
		print('[INFO]: Start to cache, file save in <%s>' % os.path.join(savepath, savename))
		try:
			os.system('{}/utils/ffmpeg.exe -i {} -c copy {}'.format(os.getcwd(), '"%s"' % live_url, os.path.join(savepath, savename)))
		except:
			os.system('ffmpeg.exe -i {} -c copy {}'.format('"%s"' % live_url, os.path.join(savepath, savename)))


if __name__ == '__main__':
	roomid = input('Please enter roomid(Example: 714420):')
	douyuTV().cache(roomid)