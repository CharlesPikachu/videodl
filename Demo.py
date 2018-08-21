# 代码仅供学习交流，不得用于商业/非法使用
# 作者：Charles
# 公众号：Charles的皮卡丘
# 视频下载器-Demo版
# 目前支持的平台:
# 	网易云课堂: wangyiyun.wangyiyun()
# 	音悦台: yinyuetai.yinyuetai()
# 	B站: bilibili.bilibili()
# 	知乎: zhihu.zhihu()
# 	斗鱼: douyu.douyu()
import os
import threading
from platforms import *
from utils.utils import *
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk


# 下载器类
class Download_Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Download_Thread, self).__init__(*args, **kwargs)
		self.__pause = threading.Event()
		self.__pause.clear()
		self.__running = threading.Event()
		self.__running.set()
		self.flag = False
		# 对应关系:
		# 	网易云课堂 -> '1'
		# 	音悦台 -> '2'
		# 	B站 -> '3'
		# 	知乎 -> '4'
		#	斗鱼 -> '5'
		self.engine = None
		self.url = None
		self.savepath = './videos'
	def run(self):
		while self.__running.isSet():
			self.__pause.wait()
			self.flag = True
			if self.engine == '1':
				self.show_start_info()
				try:
					res = wangyiyun.wangyiyun().get(self.url, savepath=self.savepath, app='demo')
					if res != 200:
						raise RuntimeError('url request error...')
				except:
					self.show_parse_error()
				self.show_end_info(savepath=self.savepath)
			elif self.engine == '2':
				self.show_start_info()
				try:
					res = yinyuetai.yinyuetai().get(self.url, savepath=self.savepath, app='demo')
					if res != 200:
						raise RuntimeError('url request error...')
				except:
					self.show_parse_error()
				self.show_end_info(savepath=self.savepath)
			elif self.engine == '3':
				self.show_start_info()
				try:
					res = bilibili.bilibili().get(self.url, savepath=self.savepath, app='demo')
					if res != 200:
						raise RuntimeError('url request error...')
				except:
					self.show_parse_error()
				self.show_end_info(savepath=self.savepath)
			elif self.engine == '4':
				self.show_start_info()
				try:
					res = zhihu.zhihu().get(self.url, savepath=self.savepath, app='demo')
					if res != 200:
						raise RuntimeError('url request error...')
				except:
					self.show_parse_error()
				self.show_end_info(savepath=self.savepath)
			elif self.engine == '5':
				self.show_start_info()
				try:
					res = douyu.douyu().get(self.url, savepath=self.savepath, app='demo')
					if res != 200:
						raise RuntimeError('url request error...')
				except:
					self.show_parse_error()
				self.show_end_info(savepath=self.savepath)
			else:
				title = '解析失败'
				msg = '平台选项参数解析失败！'
				messagebox.showerror(title, msg)
			self.pause()
	def pause(self):
		self.__pause.clear()
	def resume(self):
		self.__pause.set()
	def stop(self):
		self.__running.clear()
	def show_start_info(self):
		title = '开始下载'
		msg = '搜索平台: {}\n已开始下载{}，请耐心等待。'.format(self.engine, self.url)
		messagebox.showinfo(title, msg)
	def show_end_info(self, savepath='./videos'):
		title = '下载成功'
		msg = '{}下载成功。'.format(self.url)
		messagebox.showinfo(title, msg)
	def show_parse_error(self):
		title = '解析失败'
		msg = '视频链接解析失败！'
		messagebox.showerror(title, msg)
t_download = Download_Thread()


# 视频转换类
class Transfer_Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Transfer_Thread, self).__init__(*args, **kwargs)
		self.__pause = threading.Event()
		self.__pause.clear()
		self.__running = threading.Event()
		self.__running.set()
		self.flag = False
		self.origin_file = None
		self.target_format = None
		self.savepath = 'results'
	def run(self):
		while self.__running.isSet():
			self.__pause.wait()
			self.flag = True
			title = '开始转换'
			msg = '已开始转换视频，请耐心等待。'
			messagebox.showinfo(title, msg)
			try:
				result = transfer(origin_file=self.origin_file, target_format=self.target_format, savepath=self.savepath)
				if result is False:
					raise RuntimeError('origin_file unsupported...')
			except:
				title = '转换失败'
				msg = '视频转换失败！'
				messagebox.showerror(title, msg)
			self.pause()
	def pause(self):
		self.__pause.clear()
	def resume(self):
		self.__pause.set()
	def stop(self):
		self.__running.clear()
t_transfer = Transfer_Thread()


# 下载器
def downloader(options, op_engine_var, en_videourl_var):
	engine = str(options.index(str(op_engine_var.get())) + 1)
	t_download.engine = engine
	t_download.url = str(en_videourl_var.get())
	if t_download.flag is False:
		t_download.start()
	t_download.resume()


# 转换器
def converter(en_originvideo_var, op_tarformat_var):
	t_transfer.origin_file = str(en_originvideo_var.get())
	t_transfer.target_format = str(op_tarformat_var.get())
	if t_transfer.flag is False:
		t_transfer.start()
	t_transfer.resume()


# 选择视频
def ChoiceVideo(en_originvideo):
	filepath = filedialog.askopenfilename()
	en_originvideo.delete(0, END)
	en_originvideo.insert(INSERT, filepath)


# 关于作者
def ShowAuthor():
	title = '关于作者'
	msg = '作者: Charles\n公众号: Charles的皮卡丘\nGithub: https://github.com/CharlesPikachu/Video-Downloader'
	messagebox.showinfo(title, msg)


# 退出程序
def stopDemo(root):
	t_download.stop()
	t_transfer.stop()
	root.destroy()
	root.quit()


# 主界面
def Demo(options):
	assert len(options) > 0
	# 初始化
	root = Tk()
	root.title('视频下载器V1.2——公众号:Charles的皮卡丘')
	root.resizable(False, False)
	root.geometry('600x375+400+120')
	image_path = './bgimgs/bg1_demo.jpg'
	bgimg = Image.open(image_path)
	bgimg = ImageTk.PhotoImage(bgimg)
	lb_bgimg = Label(root, image=bgimg)
	lb_bgimg.grid()
	# Menu
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=False)
	filemenu.add_command(label='退出', command=lambda: stopDemo(root), font=('楷体', 10))
	menubar.add_cascade(label='文件', menu=filemenu)
	filemenu = Menu(menubar, tearoff=False)
	filemenu.add_command(label='关于作者', command=ShowAuthor, font=('楷体', 10))
	menubar.add_cascade(label='更多', menu=filemenu)
	root.config(menu=menubar)
	# Label组件(标题)
	lb_title1 = Label(root, text='视频下载', font=('楷体', 15), bg='white')
	lb_title1.place(relx=0.5, rely=0.05, anchor=CENTER)
	lb_title2 = Label(root, text='视频转换', font=('楷体', 15), bg='white')
	lb_title2.place(relx=0.5, rely=0.55, anchor=CENTER)
	# 视频下载部分:
	# 	Label+Entry组件(视频地址)
	lb_videourl = Label(root, text='视频地址:', font=('楷体', 10), bg='white')
	lb_videourl.place(relx=0.1, rely=0.15, anchor=CENTER)
	en_videourl_var = StringVar()
	en_videourl = Entry(root, textvariable=en_videourl_var, width=55, fg='gray', relief=GROOVE, bd=3)
	en_videourl.insert(0, 'http://study.163.com/course/courseMain.htm?courseId=1003842018')
	en_videourl.place(relx=0.49, rely=0.15, anchor=CENTER)
	# 	Label+OptionMenu组件(搜索平台)
	lb_engine = Label(root, text='搜索平台:', font=('楷体', 10), bg='white')
	lb_engine.place(relx=0.1, rely=0.25, anchor=CENTER)
	op_engine_var = StringVar()
	op_engine_var.set(options[0])
	op_engine = OptionMenu(root, op_engine_var, *options)
	op_engine.place(relx=0.26, rely=0.25, anchor=CENTER)
	# 	Button组件(下载与退出)
	bt_download = Button(root, text='下载视频', bd=2, width=15, height=2, command=lambda: downloader(options, op_engine_var, en_videourl_var), font=('楷体', 10))
	bt_download.place(relx=0.26, rely=0.38, anchor=CENTER)
	bt_quit = Button(root, text='退出程序', bd=2, width=15, height=2, command=lambda: stopDemo(root), font=('楷体', 10))
	bt_quit.place(relx=0.52, rely=0.38, anchor=CENTER)
	# 视频转换部分:
	# 	Label+Entry+Button组件(视频路径)
	lb_originvideo = Label(root, text='视频路径:', font=('楷体', 10), bg='white')
	lb_originvideo.place(relx=0.1, rely=0.65, anchor=CENTER)
	en_originvideo_var = StringVar()
	en_originvideo = Entry(root, textvariable=en_originvideo_var, width=55, fg='gray', relief=GROOVE, bd=3)
	en_originvideo.insert(0, '请输入/选择视频路径')
	en_originvideo.place(relx=0.49, rely=0.65, anchor=CENTER)
	bt_choice = Button(root, text='打开', bd=1, width=5, height=1, command=lambda: ChoiceVideo(en_originvideo), font=('楷体', 10))
	bt_choice.place(relx=0.86, rely=0.65, anchor=CENTER)
	# 	Label+OptionMenu组件(目标格式)
	lb_tarformat = Label(root, text='目标格式:', font=('楷体', 10), bg='white')
	lb_tarformat.place(relx=0.1, rely=0.75, anchor=CENTER)
	options_format = ['mp4', 'flv', 'avi']
	op_tarformat_var = StringVar()
	op_tarformat_var.set(options_format[0])
	op_tarformat = OptionMenu(root, op_tarformat_var, *options_format)
	op_tarformat.place(relx=0.22, rely=0.75, anchor=CENTER)
	# 	Button组件(视频转换)
	bt_transfer = Button(root, text='开始转换', bd=2, width=15, height=2, command=lambda: converter(en_originvideo_var, op_tarformat_var), font=('楷体', 10))
	bt_transfer.place(relx=0.52, rely=0.75, anchor=CENTER)
	root.mainloop()



if __name__ == '__main__':
	options = ["1.网易云课堂", "2.音悦台", "3.B站", "4.知乎", "5.斗鱼"]
	Demo(options)