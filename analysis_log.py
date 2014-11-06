#coding=utf-8
import sys
import re
from httplib2 import Http


base_site = 'http://dianhua.itil.com'
url = 'http://dianhua.itil.com/qclog/clientlog'
headers = {
'cookie' : 'webpy_session_id=ce9a076a50e7a9827111a9e244ffb67b8754cdfa'
}

#cookie = 'webpy_session_id=ce9a076a50e7a9827111a9e244ffb67b8754cdfa; SpryMedia_DataTables_str60817_clientlog=%7B%22iCreate%22%3A1415277843663%2C%22iStart%22%3A0%2C%22iEnd%22%3A1%2C%22iLength%22%3A10%2C%22aaSorting%22%3A%5B%5B0%2C%22asc%22%2C0%5D%5D%2C%22oSearch%22%3A%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%22aoSearchCols%22%3A%5B%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%5D%2C%22abVisCols%22%3A%5Btrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%5D%7D; SpryMedia_DataTables_str29916_clientlog=%7B%22iCreate%22%3A1415277861068%2C%22iStart%22%3A0%2C%22iEnd%22%3A1%2C%22iLength%22%3A10%2C%22aaSorting%22%3A%5B%5B0%2C%22asc%22%2C0%5D%5D%2C%22oSearch%22%3A%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%22aoSearchCols%22%3A%5B%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%5D%2C%22abVisCols%22%3A%5Btrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%5D%7D; SpryMedia_DataTables_str62091_clientlog=%7B%22iCreate%22%3A1415278125357%2C%22iStart%22%3A0%2C%22iEnd%22%3A1%2C%22iLength%22%3A10%2C%22aaSorting%22%3A%5B%5B0%2C%22asc%22%2C0%5D%5D%2C%22oSearch%22%3A%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%22aoSearchCols%22%3A%5B%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%2C%7B%22bCaseInsensitive%22%3Atrue%2C%22sSearch%22%3A%22%22%2C%22bRegex%22%3Afalse%2C%22bSmart%22%3Atrue%7D%5D%2C%22abVisCols%22%3A%5Btrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%2Ctrue%5D%7D'

def get_req_with_cookie():
    h = Http()
    return h

def get_file(url,filename):
    h = get_req_with_cookie()
    res,content = h.request(url,headers=headers)
    p(filename)
    p(len(content))
    with open(filename,"w+") as f:
        f.write(content)
        p("done in %s" % filename)


def get_log_by_imei_and_date(imei,date):
    body = 'time=%s&keyword=%s' %(date,imei)
    h = get_req_with_cookie()
    res,content = h.request(url,"POST",headers=headers,body=body)
    '''
    print res
    print content.decode("utf-8").encode("gbk")
    '''
    [push,forground] = map(lambda n: base_site + n, detect_record(content))
    get_file(push,imei + "__" + date + "push.txt")
    get_file(forground,imei + "__" + date + "for.txt");




def localize(s):
    return s.decode("utf-8").encode("gbk")

def detect_record(s):
    if not re.findall(r'div.*none.*red',s):
        raise BaseException(u'no record for that day')
    else:
        push = re.findall(r'/qclog/q\?v=d.*?push.log',s)
        forground = re.findall(r'/qclog/q\?v=d.*?forground.log',s)
        if push and forground:
            p("OK: found both logfile")
        else:
            raise BaseException("E:forground %s , push %s" % (forground,push))
    return [push[0],forground[0]]


def p(s):
    print s

def main():
    p(sys.argv)
    get_log_by_imei_and_date('357485031326269','20141105')


if __name__ == '__main__':
    main()



