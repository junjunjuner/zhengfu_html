import requests
import re
import chardet
from bs4 import BeautifulSoup as bf
import time
from selenium import webdriver
import csv
import xlwt
#4.国务院    完成
#最新政策
#将静态网页转为html文件
import urllib.request


def getHtml(url):
  html = urllib.request.urlopen(url).read()
  return html


def saveHtml(file_name, file_content):
  #    注意windows文件命名的禁用符，比如 /
  with open(file_name.replace('/', '_') + ".html", "wb") as f:
    #   写文件用bytes而不是str，所以要转码
    f.write(file_content)

url = 'http://sousuo.gov.cn/column/30469/0.htm'     #/0表示第几页
text = requests.get(url).text
href_list = re.findall('<a href="(.*?)" target="_blank">(.*?)</a>',text)
date_list = re.findall('<span class="date">(.*?) </span>',text)

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('国务院',cell_overwrite_ok=True )
header = [u'标题', u'正文', u'附件', u'政策来源处', u'发布日期', u'政策链接']
i = 0
# 写表头
for each_header in header:
    worksheet.write(0, i, each_header)
    i += 1
row = 1
for i in range(len(href_list)):
    href = href_list[i][0]
    title = href_list[i][1]
    date = date_list[i]
    # print(href,title,date)
    if re.findall('2018.04',date):
        html = getHtml(href)
        saveHtml(title, html)
        print("下载成功")

        # 向excel表插入超链接
        i = 0
        content = [title, "", "", "国务院（最新政策）", date, href]
        for each_header in content:
            worksheet.write(row, i, each_header)
            i += 1
        link = 'HYPERLINK("%s";"%s")' % (str(title) + '.html', str(title))
        worksheet.write(row, 1, xlwt.Formula(link))
        # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com
        row = row + 1
workbook.save('政府政策公告信息.xls')