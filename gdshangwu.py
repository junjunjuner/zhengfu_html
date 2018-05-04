#将动态加载的页面转为html文件
import urllib.request
from selenium import webdriver
import time
from bs4 import BeautifulSoup as bf
import requests
import re
import csv
import xlwt

def getHtml(url):
    driver = webdriver.Chrome('/home/260199/chrome/chromedriver')
    driver.get(url)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    time.sleep(3)
    html_str = driver.page_source
    print(html_str)
    # html = urllib.request.urlopen(url).read()
    html = bytes(html_str, encoding="utf8")        #转码
    return html


def saveHtml(file_name, file_content):
  #    注意windows文件命名的禁用符，比如 /
  with open(file_name.replace('/', '_') + ".html", "wb") as f:
    #   写文件用bytes而不是str，所以要转码
    f.write(file_content)

url = 'http://www.gdcom.gov.cn/zwgk/gggs/'
req = requests.get(url)
req.encoding='utf-8'
a = re.compile("<a href=\"(.*?)\" title='(.*?)'>(.*?)</a><span>(.*?) </span>")
title_list = re.findall(a,req.text)
f = open('last_href.txt','w')
f.write('http://www.gdcom.gov.cn/zwgk/gggs/'+title_list[1][0])

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('广东省商务厅',cell_overwrite_ok=True )
header = [u'标题', u'正文', u'附件', u'政策来源处', u'发布日期', u'政策链接']
i = 0
# 写表头
for each_header in header:
    worksheet.write(0, i, each_header)
    i += 1
row = 1
for titles in title_list:
    href = 'http://www.gdcom.gov.cn/zwgk/gggs/' + titles[0]
    title = titles[1]
    date = titles[-1]
    # if re.findall('2018-03', date):
    html = getHtml(href)
    saveHtml(title, html)
    print("下载成功")

    #向excel表插入超链接
    i = 0
    content = [title,"", "", "广东省商务厅（公告公示）", date, href]
    for each_header in content:
        worksheet.write(row, i, each_header)
        i += 1
    link = 'HYPERLINK("%s";"%s")' % (str(title)+'.html', str(title))
    worksheet.write(row, 1, xlwt.Formula(link))
    # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com
    row = row + 1
workbook.save('政府政策公告信息.xls')


# #广东省商务厅
# #公告公示
# url = 'http://www.gdcom.gov.cn/zwgk/gggs/'
# req = requests.get(url)
# req.encoding='utf-8'
# a = re.compile("<a href=\"(.*?)\" title='(.*?)'>(.*?)</a><span>(.*?) </span>")
# title_list = re.findall(a,req.text)
# for titles in title_list:
#     href = 'http://www.gdcom.gov.cn/zwgk/gggs/' + titles[0]
#     title = titles[1]
#     date = titles[-1]
#     if re.findall('2018-04',date):
#         print(href,title,date)
#         req_gonggao = requests.get(href)
#         req_gonggao.encoding = 'utf-8'
#         soup = bf(req_gonggao.text,'lxml')
#         content = soup.find('div',class_='zw-right-xl ').get_text()
#         s = re.compile('(.*?)ont-size:10.5pt;|}|\n\n')
#         content = re.sub(s,'',content)
#         with open("政府政策公告.csv", "a") as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow([title, content, "", "广东省商务厅（公告公示）", date, href])