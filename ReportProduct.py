# -*- coding: utf-8 -*-

NO_ACK_FILE  = "noack"
RECONNECT_FILE = "reconnect"
REASON_TABLE = {
	10009:u'ENetworkChange 网络接入点切换',
	10001:u'ERemoteClosed server端主动关闭',
	10002:u'EUnknownErr 未分类错误',
	10011:u'ENetworkLost 没有网络接入点',
	20001:u'EProcessStart 进程重启',
	10004:u'EDecodeError 长连接包头解失败了',
	10003:u'ENoopTimeout 心跳包超时',
	10016:u'ELinkCheckTimeout 重连认证失败',
	20000:u'EReboot 机器重启',
	10008:u'ETaskTimeout 任务超时',
	113:u'ENoRouteToHost ',
	104:u'EConnReset',
	110:u'TimedOut'
}


def read_reconnect_log(filename):
	reconnect_log = {}
	with open(filename,'r') as report:
		for line in report:
			col = line.split(",")
			if(len(col) < 10):
				continue
			report_date = col[9]
			uuid = int(col[10])
			date = col[16].split("&")
			if len(date) > 3:
				end_time = date[0]
				start_time = date[1]
				reason = date[2]
				record = reconnect_log.get(uuid,[{"d":0,"c":0,"r":0}])
				record.append({"c":int(start_time),"d":int(end_time),"r":int(reason)})
				record = sorted(record,key=getkey)
				reconnect_log[uuid] = record
	return reconnect_log


def read_invite_log(filename):
	invite_log = {}
	with open(filename,"r")  as lines:
		for line in lines:
			vals = line.split("\t")
			if len(vals) > 3:
				called = int(vals[3])
				call_time = int(vals[5]) * 1000
				l = invite_log.get(called,[])
				l.append(call_time)
				invite_log[called] = l
	return invite_log


def getkey(item):
	return item["c"]


def p(x):
	print x


def main():
	reconnect = read_reconnect_log(RECONNECT_FILE)
	no_ack = read_invite_log(NO_ACK_FILE)
	p("info:xici %d,canson %d" %(len(no_ack),len(reconnect)))
	total,reasons = disconnect_reason(reconnect)
	print "id	,count	,per 	,desc"
	for r,cnt in reasons.items():
		if r == 0:
			continue
		print "%d 	,%d 	,%.4f 	,%s"  %(r,cnt,float(cnt)/total,REASON_TABLE[int(r)].encode("utf-8"))


	for k,val in no_ack.items(): #k[uid] val[calltime,calltime1]
		online = reconnect.get(k,[])
		for call_time in val:
			online = reconnect.get(k,[])
			length = len(online)
			if length > 3:
				for i in range(1,length):
					c = online[i]["c"]	#connect time
					d = online[i]["d"]	#disconnect time_val
					#print "%d content %s" %(k,online[i])
					if c > call_time:
						if d > call_time:
							pass
							# print "uid:%d calltime: %d online for [c:%d,d:%d]" %(k,call_time,online[i-1]["c"],online[i]["d"])
						else:
							# print "uid:%d calltime :%d offline for [d:%d,c:%d] delta:%d" %(k,call_time,d,c,(call_time - d)/(1000*60))
							delta = (call_time - d) / (60 * 10000)
							print "%d 	%d 	%d 	%d 	%d 	%s 	%s" %(k,call_time,d,c,delta,delta < 4.5,delta < 11.5)



						break
					if i == length -1 and c <= call_time:
						pass
						#print "no result for call_time:%d de:%s" %(call_time,online)



def disconnect_reason(mm):
	total = 0
	percentage = {}
	for uid,value_list in mm.items():
		for item in value_list:
			reason = item["r"]
			count = percentage.get(reason,0)
			count = count + 1
			percentage[item["r"]] = count
			if reason != 0:
				total = total + 1
	return (total,percentage)




if __name__ == '__main__':
	main()









