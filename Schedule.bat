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
from os.path import isfile
from dateutil.parser import parse
from sys import argv

LEAVE_DATE_COL = u'出院日期'
TPL_FILE = os.path.join(os.path.dirname(sys.argv[0]),'python3/template.html')

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

def move_over_iter(sheet,position):
	record = []
	rows = sheet.nrows
	cur = parse("")
	record.append(sheet.row(0))
	for pos in range(1,rows):
		cell = sheet.cell(pos,position)
		try:
			leave_time = parse(cell.value)
			days  = (cur - leave_time).days
			if days in [30,60,90,365]:
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
	cwd = os.path.dirname(os.getcwd())
	print("使用目录 %s 作为存放Excel的目录\n" % cwd)
	csv_files = {}
	files = get_all_files(cwd)

	print ("共发现%d个excel文件:" %len(files))
	print ("\n".join(files))
	print ("\n")

	for f in files:
		try:
			sheet = get_sheets_by_name(f,0)
			idx = determine_leave_col(sheet)
			if idx != -1:
				should_visit = move_over_iter(sheet,idx)
				csv_files[f] = should_visit
			else:
				print("文件 %s 中未找到 %s 栏" %(f,LEAVE_DATE_COL))
		except :
			pass

	filename = os.path.join(cwd,str(parse("").date()) + ".html");
	format_to_html(cwd,csv_files)

	print("结果写入文件%s 中\n" % filename)
	print("按照任意键结束")
	input()



if __name__ == '__main__':
	main()
