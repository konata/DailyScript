#coding=utf-8
import urllib3
import sys
import re
import traceback
from time import gmtime,strftime


FOUND_PATTERN = r'div.*display:none;color:red'
FORGEGROUND_PATTERN = r'/qclog/q\?v=d.*?forground.log'
PUSH_PATTERN = u'/qclog/q\?v=d.*?pblog_push.log'
COOKIE = u"webpy_session_id=694e23e930e6e5c517c3f5414e67629971575b93; SpryMedia_DataTables_str25433_clientlog=%7B%22iCreate%22%3A1416627537995%2C%22iStart%22%3A0%2C%22iEnd%22%3A1%2C%22iLength%22%3A10%2C%22aaSorting%22%3A%5B%5B0%2C%22asc%22%2C0%5D%5D%2C%22oSearch%22%3A%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%22aoSearchCols%22%3A%5B%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%5D%2C%22abVisCols%22%3A%5Btrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%5D%7D; SpryMedia_DataTables_str32408_clientlog=%7B%22iCreate%22%3A1416627543183%2C%22iStart%22%3A0%2C%22iEnd%22%3A1%2C%22iLength%22%3A10%2C%22aaSorting%22%3A%5B%5B0%2C%22asc%22%2C0%5D%5D%2C%22oSearch%22%3A%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%22aoSearchCols%22%3A%5B%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%5D%2C%22abVisCols%22%3A%5Btrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%5D%7D; SpryMedia_DataTables_str27806_clientlog=%7B%22iCreate%22%3A1416627547162%2C%22iStart%22%3A0%2C%22iEnd%22%3A1%2C%22iLength%22%3A10%2C%22aaSorting%22%3A%5B%5B0%2C%22asc%22%2C0%5D%5D%2C%22oSearch%22%3A%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%22aoSearchCols%22%3A%5B%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%5D%2C%22abVisCols%22%3A%5Btrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%5D%7D"
ADDRESS = u"http://dianhua.itil.com/qclog/clientlog"
SITE = u"http://dianhua.itil.com"

class LogRetriever:
	def __init__(self):
		self.pool = urllib3.PoolManager()

	def GetLogAddress(self,imei,date):
		body = "time=%s&keyword=%s" %(date,imei)
		result = {}
		result["imei"] = imei
		result["date"] = date
		try:
			resp = self.pool.urlopen("POST",ADDRESS,headers={"COOKIE":COOKIE},body=body)
			text = result['txt'] = resp.data

			if re.findall(FOUND_PATTERN,text):
				fore = re.findall(FORGEGROUND_PATTERN,text)
				if fore:
					result["fore"] = SITE + fore[0]
		
				push = re.findall(PUSH_PATTERN,text)
				if push:
					result["push"] = SITE + push[0]

				print result["push"]
				self.WriteBack(result,True)

			else:
				self.Fatal("no log for imei:%s and date:%s" %(imei,date))
				self.WriteBack(result,False)

		except Exception as e:
			self.Fatal("can not get imei:%s for date:%s Reason:%s" %(imei,date,str(e)))
			traceback.print_exc(file=sys.stdout)
			result['txt'] = ''
			self.WriteBack(result,False)


	def Fatal(self,s):
		print s


	def GetLog(self,imei,date):
		pass


	def WriteBack(self,result,succ):	
		if succ:
			for x in "fore push".split(" "):
				filename = result["imei"] + "__" + result["date"] + "__" + x
				log_content = self.pool.urlopen("GET",result[x],headers={"COOKIE":COOKIE}).data

				with open(filename,"w") as log:
					#log.write("\n".join([line for line in log_content if len(line.strip()) > 0]))
					log.write("".join(log_content))
		else:
			filename = result['imei'] + "_failed"
			with open(filename,"w") as log:
				log.write("failed!")
		


def main():
	if len(sys.argv) < 2:
		print "Usage:python GetLog.py imeifile [date]"
	else:
		imei_files = sys.argv[1]
		imeis =  [line.strip() for line in open(imei_files,"r") if len(line.strip()) > 0]

		if(len(sys.argv) < 3):
			d = strftime("%Y%m%d",gmtime())
		else:
			d = sys.argv[2]

		log_downloader = LogRetriever()

		for imei in imeis:
			log_downloader.GetLogAddress(imei,d)

		print "Done"



if __name__ == '__main__':
	main()



