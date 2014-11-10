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

def move_over_iter(sheet,position,days):
    record = []
    rows = sheet.nrows
    cur = parse("")
    record.append(sheet.row(0))
    for pos in range(1,rows):
        cell = sheet.cell(pos,position)
        try:
            leave_time = parse(cell.value)
            day = (cur - leave_time).days
            if day < 5:
                print(days)
                print(day)
                print("==========")

            if day in days:
                print("fucku!!!")
                record.append(sheet.row(pos))
        except :
            pass
    return record


def format_to_html(dirname,list_of_files):
    tpl = '''
        <h3><center>_title_</center></h3>
                <table class="table">
                    _html_
                </table>
                <br/> <br/> <br/>
    '''
    html = []
    for filename,file_content in list_of_files.items():
        # key filename
        header,content = file_content[0],file_content[1:]
        header_html = '<thead><tr>' + " ".join(map(lambda v : '<th>' + str(v.value).replace(' ','') + '</th>' , header)) + '</tr></thead>'
        content_html = '<tbody>' + " ".join(map(lambda col : '<tr>' + "".join(map(lambda n : '<td>' + str(n.value).replace(' ','') +'</td>', col))  + '</tr>', content)) + '</tbody>'
        html.append(tpl.replace('_html_',header_html + content_html).replace('_title_',filename))

    # read template
    with open(TPL_FILE,"r") as template:
        date_str = str(parse('').date())
        tpl_content = template.read().replace('_html_',''.join(html)).replace('_date_',date_str)
        with open(os.path.join(os.path.dirname(sys.argv[0]),date_str) + ".html","w+",encoding="utf-8") as log_file:
            log_file.write(tpl_content)



def main():
    print("使用目录 %s 作为存放Excel的目录\n" % CWD)
    csv_files = {}
    files = get_all_files(CWD)

    print ("共发现%d个excel文件:" %len(files))
    print ("\n".join(files))
    print ("\n")

    custom_date = parse_ini()
    for f in files:
        try:
            sheet = get_sheets_by_name(f,0)
            idx = determine_leave_col(sheet)
            days = find_days_for_file(f,custom_date)
            if idx != -1:
                should_visit = move_over_iter(sheet,idx,days)
                csv_files[f + "(" + " , ".join(str(day) for day in days) + ")"] = should_visit
            else:
                print("文件 %s 中未找到 %s 栏" %(f,LEAVE_DATE_COL))
        except xlrd.biffh.XLRDError:
            pass

    filename = os.path.join(CWD,str(parse("").date()) + ".html");
    format_to_html(CWD,csv_files)
    print("结果写入文件%s 中\n" % filename)
    print("按照任意键结束")
    input()


def find_days_for_file(filename,maps):
    for key,value in maps.items():
        if key in os.path.basename(filename):
            return value
    return DEFAULT_INTERVAL


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



