'''
cls
@echo off
cd/d "%~dp0"

set path=%~dp0python3\DLLs;%path%

cd python3
python.exe "%~f0"

goto:eof
'''

# coding=utf-8
import xlrd
import os
import sys
import configparser
from os.path import isfile
from dateutil.parser import parse
from sys import argv
from datetime import *

LEAVE_DATE_COL = u'出院日期'
CWD = os.path.join(os.path.dirname(sys.argv[0]))
TPL_FILE = os.path.join(CWD,'python3/template.html')
INI_FILE = os.path.join(CWD,'config.ini')
CFG_KEY = "interval"
DEFAULT_INTERVAL = [30,60,90,365]

def get_all_files(folder):
    return [os.path.join(folder,f) for f in os.listdir(folder) if f.endswith('.xls')]

def get_sheets_by_name(fname,idx):
    wb = xlrd.open_workbook(fname)
    return wb.sheet_by_index(idx)

def determine_leave_col(sheet):
    row = sheet.row(0)
    position = -1 # default col count for leave date
    for idx, cell in enumerate(row):
        if cell.value.replace(" ","").find(LEAVE_DATE_COL) != -1:
            position = idx
    return position

def move_over_iter(sheet,position,days,for_day):
    record = []
    rows = sheet.nrows
    record.append(sheet.row(0))
    for pos in range(1,rows):
        cell = sheet.cell(pos,position)
        try:
            leave_time = parse(cell.value)
            day = (for_day - leave_time.date()).days
            echo ("found day : " + str(day) + " days: " + str(days))
            if day in days:
                echo(sheet.row(pos))
                record.append(sheet.row(pos))
        except :
            print(sys.exc_info())
            pass
    return record


def main():
    echo("使用目录 %s 作为存放Excel的目录\n" % CWD)
    csv = {}
    files = get_all_files(CWD)

    echo("共发现%d个excel文件:" %len(files))
    echo("\n".join(files))
    echo("\n")

    today = date.today()
    begin = date(today.year,today.month,1)
    ini = parse_ini()

    for xls in files:
        try:
            sheet = get_sheets_by_name(xls,0)
            idx = determine_leave_col(sheet)
            ini_days = find_days_for_file(xls,ini)
            if idx != -1:
                for itr_days in (today - timedelta(n) for n in range((today - begin).days)):
                    should_visit = move_over_iter(sheet,idx,ini_days,itr_days)
                    csv.setdefault(itr_days,{}).setdefault(xls + "(" + " , ".join(str(day) for day in ini_days) + ")",should_visit)
            else:
                echo("文件 %s 中未找到 %s 栏" %(xls,LEAVE_DATE_COL))
        except xlrd.biffh.XLRDError:
            pass
    htmlfy(csv,begin,today)
    echo("结果写入文件  %s to %s.html 中\n" % (begin,today))
    echo("按照任意键结束")
    input()


def format_each_day(record_of_day,day):
    tpl = '''
        <h3><center>_title_</center></h3>
                <table class="table">
                    _html_
                </table>
                <br/> <br/> <br/>
    '''
    html = []
    for filename,file_content in record_of_day.items():
        # key filename
        header,content = file_content[0],file_content[1:]
        header_html = '<thead><tr>' + " ".join(map(lambda v : '<th>' + str(v.value).replace(' ','') + '</th>' , header)) + '</tr></thead>'
        content_html = '<tbody>' + " ".join(map(lambda col : '<tr>' + "".join(map(lambda n : '<td>' + str(n.value).replace(' ','') +'</td>', col))  + '</tr>', content)) + '</tbody>'
        html.append(tpl.replace('_html_',header_html + content_html).replace('_title_',filename))


    return "<br>".join(html)
    '''
    joined_html = tpl.replace('_html_',''.join(html)).replace('_date_',str(day))
    return joined_html
    '''

def htmlfy(csv,begin,today):
    filename = "%s to %s.html" % (begin,today)
    sep_for_day = '''
        <br/>
        <center><h1 style="color:red;font-size:20px">_date_的回访记录</h1></center>
        _html_
        <br/>
        <br/>
        <br/>
    '''

    entire = ''
    for day,record in sorted(csv.items()):
        htmls = format_each_day(record,day)
        entire += sep_for_day.replace('_date_',str(day)).replace('_html_',htmls)

    # read template
    with open(TPL_FILE,"r") as template:
        content = template.read().replace('_html_',entire)
        with open(os.path.join(os.path.dirname(sys.argv[0]),filename),"w+",encoding="utf-8") as dist:
            dist.write(content)



def find_days_for_file(filename,maps):
    for key,value in maps.items():
        if key in os.path.basename(filename):
            return value
    return DEFAULT_INTERVAL


def echo(content):
    print(content)

def parse_ini():
    user_defs = {}
    try:
        instance = configparser.ConfigParser()
        instance.read(INI_FILE)
        for sec in instance.sections():
            user_defs[sec.strip()] = [int(l.strip()) for l in instance[sec][CFG_KEY].split(",") if len(l.strip()) > 0 ]
    except :
        pass
    return user_defs


if __name__ == '__main__':
    main()



