# coding:utf-8
from __future__ import print_function
import requests
from requests import Session
import PIL
import pyocr
from PIL import Image
import StringIO

"""
	take cookie from GLOBAL object,
	when expired, replace or retrieve & save the GLOBAL session,

steps:
	1. detect cookie,
	2. ocr and regain cookie (captcha and login)
	3. start working threads 
"""




CAPTCHA_URL = "https://www.bmfinn.com/catcha/captchaImage"
PROXIES = {'http':'http://127.0.0.1:1090','https':'http://127.0.0.1:1090'}

def dump(*args):
	[print(arg) for arg in args]


class OCR:
	def __init__(self,image):
		self.image = image
		self.width,self.height = image.size
		self.pix = image.load()
		self.remain_blur_times = 10
		self.ocr = pyocr.get_available_tools()[0]

	def blur():
		[self.__blur_pixel(x,y) for x in xrange(1,self.width-1) for y in xrange(1,self.height-1) if reduce(operator.add,self.pix[(x,y)],0) < 500]

	def __blur_pixel(x,y):
		top = self.pix[(x,y+1)]
		bottom = self.pix[(x,y-1)]
		self.pix[(x,y)] = tuple([(top[i] + bottom[i]) / 2 for i in (0,1,2)])
		
	def identify_image(self,remain_blur_times = 10):
		res = self.ocr.image_to_string(self.image,builder=pyocr.tesseract.DigitBuilder())
		dump("recongnize as : " + res)
		if len(res) == 4 and re.match(ur'^\d+$',res):
			return res
		else:
			if remain_blur_times <= 0:
				raise Exception("can not recongnize image, change another") 
			self.blur()
			self.run(remain_blur_times-1)


class User:
	RunningUsers = []
	def __init__(self):
		self.session = Session()
		self.RunningUsers.append(self)

	def trim(self):
		self.RunningUsers.remove(self)

	def read_captcha(self,retry_count = 5):
		try:
			dump('read_caption',retry_count)
			self.image_response = self.session.get(CAPTCHA_URL,verify=False,proxies=PROXIES)
			dump('read_caption_done')
			image = Image.open(StringIO.StringIO(self.image_response.content))
			self.ocr = OCR(image)
			return self.identify_image()
		except Exception,e:
			dump(e)
			if retry_count >= 1:
				self.read_captcha(retry_count - 1)
			else:
				dump('failed get captcha')

	def cookie(self):
		return str(self.session.cookies)

	def login(self):
		pass

	def other_action(self):
		pass

	@classmethod
	def current_running(clz):
		return len(clz.RunningUsers)

	@classmethod
	def clear_session(clz):
		[user.shutdown for user in clz.RunningUsers]


def main():
	user  = User()
	captcha = user.read_captcha();
	dump("captcha : " + str(captcha))

if __name__ == '__main__':
	main()



