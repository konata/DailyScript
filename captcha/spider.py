# coding:utf-8
from __future__ import print_function
import requests
from requests import Session
import PIL
import pyocr
from PIL import Image
import StringIO
import traceback
import re
import operator
import tempfile 
import time

"""
  take cookie from GLOBAL object,
  when expired, replace or retrieve & save the GLOBAL session,

steps:
  1. detect cookie,
  2. ocr and regain cookie (captcha and login)
  3. list available orders
  4. submit orders
"""

"""
buy
{"code":"0","context":"已经被其他用户抢购。"}
"""


"""
LIST:
https://www.bmfinn.com//coin/buyData?pageNo=_pageNo_&timestamp=_timestamp_
<input value="9931" name="sellEpRa" type="radio">

BUY:
https://www.bmfinn.com/coin/buy?timestap=1449652284167".
timestap:1449652167397
orderId:9931
thpassword:888888
"""

CAPTCHA_URL = "https://www.bmfinn.com/catcha/captchaImage"
LOGIN_URL = "https://www.bmfinn.com/index/validate?timestap="
ORDER_LIST_URL = "https://www.bmfinn.com//coin/buyData"
SUBMIT_ORDER = "https://www.bmfinn.com/coin/buy"

"""
USERNAME = 'dzm888'
PASSWORD = '888888'
PAY_PASSWORD = '888888'
"""
USERNAME = 'lxy1978'
PASSWORD = '9151026'
PAY_PASSWORD = '915918'

PROXIES = {'http':'http://127.0.0.1:1090','https':'http://127.0.0.1:1090'}

def dump(*args):
  [print(arg) for arg in args]

def fatal(*args):
  dump(args)
  log_name = time.strftime("%m-%d-%H",time.localtime(time.time()))
  log = open(log_name,"a+")
  log.write(str(tuple(args)) + "\n")
  # [log.write(str(arg) + "\n") for arg in args]
  log.close()

class OCR:
  def __init__(self,image):
    self.image = image
    self.width,self.height = image.size
    self.pix = image.load()
    self.remain_blur_times = 10
    self.ocr = pyocr.get_available_tools()[0]

  def blur(self):
    [self.__blur_pixel(x,y) for x in xrange(1,self.width-1) for y in xrange(1,self.height-1) if reduce(operator.add,self.pix[(x,y)],0) < 500]

  def __blur_pixel(self,x,y):
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
      return self.identify_image(remain_blur_times-1)


class User:
  RunningUsers = []
  def __init__(self):
    self.session = Session()
    self.RunningUsers.append(self)

  def trim(self):
    self.RunningUsers.remove(self)

  def read_captcha(self,retry_count = 5):
    dump('***read_captcha',retry_count)
    try:
      self.image_response = self.session.get(CAPTCHA_URL,verify=False) #,proxies=PROXIES)
      dump('read_captcha_done')
      image = Image.open(StringIO.StringIO(self.image_response.content))
      filename = re.sub(ur'^.*/','',tempfile.mktemp())
      image.save(filename,"JPEG")
      self.ocr = OCR(image)
      return self.ocr.identify_image()
    except Exception,e:
      dump("captcha err:",traceback.format_exc())
      if retry_count > 0:
        return self.read_captcha(retry_count - 1)
      else:
        dump('failed get captcha')
        return ""

  def cookie(self):
    return str(self.session.cookies)

  def login(self,code,retry_count=30):
    dump('***login',retry_count)
    login_url = LOGIN_URL + str(int(time.time() * 1000))
    try:
      resp = self.session.post(login_url,data={
          'userName':USERNAME,
          'password':PASSWORD,
          'code':code
        })
      dump("login_resp",resp.content)
      if '"1"' in resp.content:
        return (True,resp.content)
      else:
        return (False,resp.content)
    except Exception ,e:
      dump("login err :" + str(retry_count) + ":",traceback.format_exc())
      if retry_count > 0:
        return self.login(code,retry_count-1)
      else:
        return (False,str(e))

  def list_available(self,retry_count=100):
    dump('***list_available',retry_count)
    try:
      resp = self.session.get(ORDER_LIST_URL,data={
        "pageNo":1,
        "timestamp":str(int(time.time()*1000))
      },allow_redirects=False)
      # dump("** list_available",re.sub(ur'^[\n\r]*$','',resp.content))
      dump("** list_available",resp.content)
      if resp.status_code == 302: # login again
        return (False,302)
      elif resp.content.find("sellEpRa") != -1: # buy items
        # <input value="9931" name="sellEpRa" type="radio">
        pattern = ur'value="(\d+)"\s+name="sellEpRa"'
        orders = re.findall(pattern,resp.content)
        return (True,orders[0]) 
      else: # refresh again
        pass
    except Exception,e:
        dump("**list_available",e)

    if retry_count > 0:
      return self.list_available(retry_count-1)
    else:
      dump("**list_available refresh over")
      return (False,1)


  def submit_order(self,order_id,code,submit_count=100):
    dump("***submit_order",order_id,submit_count)
    try:
      resp = self.session.post(SUBMIT_ORDER+"?timestamp=" + str(int(time.time()*1000)),data={
        # 'timestamp':str(int(time.time()*1000)),
        'orderId':str(order_id),
        'thpassword':PAY_PASSWORD,
        'code':code
      },allow_redirects=False)
      dump("**submit_order",resp.content)
      code = resp.status_code
      if code == 302:
        dump("submit order need login, lets try again",resp.status_code)
        return (False,302)
      else:
        return ('"1"' in resp.content,200)
    except Exception,e:
      dump("**submit_order  err",e)
      if submit_count < 0:
        return (False,0)
      else:
        return self.submit_order(order_id,code,submit_count-1)



  @classmethod
  def current_running(clz):
    return len(clz.RunningUsers)

  @classmethod
  def clear_session(clz):
    [user.shutdown() for user in clz.RunningUsers]


def main():
  user = User()
  logined = False

  while True:
    if not logined:
      captcha = user.read_captcha();
      fatal("captcha : " + str(captcha))
      if len(captcha) > 0:
        logined,login_resp = user.login(captcha)
        fatal("login_resp:",login_resp,logined)
      else:
        logined = False

    if logined:
      list_res,reason_or_id = user.list_available()
      fatal(list_res,reason_or_id)
      if list_res:
        submit_captcha = user.read_captcha(10)
        fatal("submit_captcha",submit_captcha)
        if len(submit_captcha) == 4:
          status,reason = user.submit_order(reason_or_id,submit_captcha)

          if status:
            fatal("buy ok: ",reason_or_id)
            return
            
          fatal(status,reason)
          fatal("buy order ok: " + reason_or_id if status else "buy failed~")
          logined = (logined and status != 302)
      else: #  
        logined = (logined and reason_or_id != 302)
        dump("list failed :" + str(reason_or_id))




if __name__ == '__main__':
  main()





