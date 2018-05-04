import requests
import re
import chardet
from bs4 import BeautifulSoup as bf
import time
from selenium import webdriver
import csv
import xlwt
#1.国家科学技术部
#通知通告，科技部工作
#将静态网页转为html文件
import urllib.request

headers = {
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

#得到网页源码
def getHtml(url):
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req).read()
    return html


#附件下载
def download(html,url):
    try:
        mystr = html.decode("gb2312")  # 解码
    except:
        try:
            mystr = html.decode("gbk")  # 解码
        except:
            mystr = html.decode("utf-8")
    down_name = []
    if "附件" in mystr:
        try:
            s = re.compile('<A href="\.(.*?)" target=_blank _fcksavedurl="(.*?)" OLDSRC=(.*?)>(.*?)</A>')
            pdfs = re.findall(s,mystr)
            for pdf in pdfs:
                pdf_href = url + pdf[0]
                pdf_name = pdf[-1]
                print(pdf_href)
                pdf_ress = '.' + pdf_href.split('.')[-1]          #附件后缀（判断.doc/.pdf等）
                r = requests.get(pdf_href, stream=True,headers = headers)
                # download started
                with open(pdf_name+pdf_ress, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                down_name.append(pdf_name+pdf_ress)
        except:
            s = re.compile('<A href="../../../../(.*?)" target=_self OLDSRC=(.*?)>(.*?)<BR></A>')
            pdfs = re.findall(s,mystr)
            for pdf in pdfs:
                pdf_href = 'http://www.most.gov.cn/' + pdf[0]
                pdf_name = pdf[-1]
                print(pdf_href)
                pdf_ress = '.' + pdf_href.split('.')[-1]          #附件后缀（判断.doc/.pdf等）
                r = requests.get(pdf_href, stream=True,headers = headers)
                # download started
                with open(pdf_name+pdf_ress, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
                down_name.append(pdf_name+pdf_ress)
    return down_name


#保存为html文件
def saveHtml(file_name, file_content):
  #    注意windows文件命名的禁用符，比如 /
  with open(file_name.replace('/', '_') + ".html", "wb") as f:
    #   写文件用bytes而不是str，所以要转码
    f.write(file_content)



def excel_book(header,source,urls,worksheet):
    i = 0
    # 写表头
    for each_header in header:
        worksheet.write(0, i, each_header)
        i += 1

    row = 1
    for j in range(len(urls)):
        url = urls[j]
        req = requests.get(url)
        try:
            req.encoding = 'gb2312'
        except:
            try:
                req.encoding='gbk'
            except:
                req.encoding='utf-8'
        #<font class="date">2018/01/11</font><a href="./201801/t20180111_873590.html" target="_blank">国家发展改革委有关负责人就《国务院办公厅关于推进公共资源配置领域政府信息公开的意见》答记者问</a><span class="new">
        if url == 'http://www.most.gov.cn/tztg/' or url == 'http://www.most.gov.cn/kjbgz/':
            a=re.compile(' <td class="STYLE30"><a href="./(.*?)" target="_blank" class=STYLE30>(.*?)</a>\((.*?)\)')
            href_list = re.findall(a, req.text)
            for i in range(len(href_list)):
                date = href_list[i][-1]
                href = url + href_list[i][0]
                down_href = url + href_list[i][0].split('/')[0]  # 附件下载前缀网址
                title = href_list[i][1]
                # print(href,title,date)
                if re.findall('2018-04', date):
                    html = getHtml(href)
                    print(href)
                    down_names = download(html, down_href)
                    saveHtml(title, html)
                    print("下载成功")

                    # 向excel表插入超链接
                    i = 0
                    content = [title, "", source[j], date, href, ""]
                    for each_header in content:
                        worksheet.write(row, i, each_header)
                        i += 1
                    link = 'HYPERLINK("%s";"%s")' % (str(title) + '.html', str(title))
                    worksheet.write(row, 1, xlwt.Formula(link))
                    if down_names != None:
                        x = 5
                        for down_name in down_names:
                            link = 'HYPERLINK("%s";"%s")' % (down_name, down_name)
                            worksheet.write(row, x, xlwt.Formula(link))
                            x = x + 1
                            # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com
                    row = row + 1
        elif url == 'http://www.most.gov.cn/kjjh/':
            a=re.compile('<div class="name"><a href="(.*?)" title="(.*?)"  target="_blank" >(.*?)</a></div>')
            href_list = re.findall(a,req.text)
            date_list = re.findall('<div class="time">(.*?)</div>',req.text)
            for i in range(len(href_list)):
                date = date_list[i]
                if '../' in href_list[i][0]:
                    href = 'http://www.most.gov.cn/'+href_list[i][0].replace('../','')
                elif './' in href_list[i][0]:
                    href = url + href_list[i][0].replace('./','')
                elif 'http:' in href_list[i][0]:
                    href =href_list[i][0]
                down_href = url + href_list[i][0].split('/')[0]  # 附件下载前缀网址
                title = href_list[i][1]
                # print(href,title,date)
                if re.findall('-',date):
                    if re.findall('.pdf',href) or re.findall('.doc',href) or re.findall('.xls',href):
                        r = requests.get(href, stream=True, headers=headers)
                        # download started
                        with open(title, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    f.write(chunk)
                    html = getHtml(href)
                    print(href)
                    saveHtml(title, html)
                    down_names = download(html,down_href)
                    print("下载成功")

                    # 向excel表插入超链接
                    i = 0
                    content = [title, "", source[j], date, href,""]
                    for each_header in content:
                        worksheet.write(row, i, each_header)
                        i += 1
                    link = 'HYPERLINK("%s";"%s")' % (str(title) + '.html', str(title))
                    worksheet.write(row, 1, xlwt.Formula(link))
                    if down_names!=None:
                        x = 5
                        for down_name in down_names:
                            link = 'HYPERLINK("%s";"%s")' % (down_name, down_name)
                            worksheet.write(row, x, xlwt.Formula(link))
                            x = x+1
                        # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com
                    row = row + 1



#通知通告，科技部工作
#政府信息公开（动态加载，未写）
#科技计划（与前面页面布局不同，未写）
#科技政策动态（与前面页面布局不同，未写）
urls = [
        # 'http://www.most.gov.cn/tztg/',    #通知通告
        # 'http://www.most.gov.cn/kjbgz/',   #科技部工作
        'http://www.most.gov.cn/kjjh/']     #科技计划
source = ['国家科学技术部（通知通告）','国家科学技术部（科技部工作）']
header = [u'标题', u'正文', u'政策来源处', u'发布日期', u'政策链接', u'附件']
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('国家科技部', cell_overwrite_ok=True)
excel_book(header,source,urls,worksheet)
workbook.save('政府政策公告信息.xls')