import requests
import re
import chardet
from bs4 import BeautifulSoup as bf
import time
from selenium import webdriver
import csv
import xlwt
#广东省科学技术厅      附件没改
#通知公告，政策法规解读，国家政策法规，省政策法规
#将静态网页转为html文件
import urllib.request

headers = {
    # 'Host':'www.ndrc.gov.cn',
    # 'Referer':'http://www.ndrc.gov.cn/zcfb/zcfbgg/201804/t20180409_881965.html',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

def getHtml(url):
  html = urllib.request.urlopen(url).read()
  return html

def download(html,url):
    mystr = html.decode("utf-8")  # 解码
    down_name = []
    soup = bf(mystr,'lxml')
    appendix = soup.find("span", {"id":"appendix"})
    if appendix.text.strip()!='':
        print(appendix)
        #<a target="_blank" oldsrc="W020180320396662975085.pdf" href="./W020180320396662975085.pdf"><font color="#0000ff">1.2017年度氢氟碳化物处置核查相关工作流程和要求</font>
        pdfs = re.findall('<a href="(.*?)">(.*?)</a>',str(appendix))
        for pdf in pdfs:
            pdf_href = url + pdf[0]
            pdf_name = pdf[-1]
            print(pdf_href)
            r = requests.get(pdf_href, stream=True,headers = headers)
            # download started
            with open(pdf_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            down_name.append(pdf_name)
        return down_name
    return None

def saveHtml(file_name, file_content):
  #    注意windows文件命名的禁用符，比如 /
  with open(file_name.replace('/', '_') + ".html", "wb") as f:
    #   写文件用bytes而不是str，所以要转码
    f.write(file_content)

#通知公告，政策法规解读，国家政策法规，省政策法规
urls = ['http://www.gdstc.gov.cn/zwgk/tzgg/index@1.htm','http://www.gdstc.gov.cn/zwgk/zcfg/zcjd/index@1.htm',
        'http://www.gdstc.gov.cn/zwgk/zcfg/gjzcfg/index@1.htm','http://www.gdstc.gov.cn/zwgk/zcfg/sfggz/index@1.htm']
source = ['广东省科学技术厅（政策发布）','广东省科学技术厅（政策解读）','广东省科学技术厅（国家政策法规）','广东省科学技术厅（省政策法规）']
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('发改委', cell_overwrite_ok=True)
header = [u'标题', u'正文', u'政策来源处', u'发布日期', u'政策链接', u'附件']
i = 0
# 写表头
for each_header in header:
    worksheet.write(0, i, each_header)
    i += 1
row = 1
for i in range(len(urls)):
    url = urls[i]
    req = requests.get(url,headers = headers)
    req.encoding= 'utf-8'
    soup = bf(req.text,'lxml')
    tab = soup.find('table',class_='ZIT')
    #<font class="date">2018/01/11</font><a href="./201801/t20180111_873590.html" target="_blank">国家发展改革委有关负责人就《国务院办公厅关于推进公共资源配置领域政府信息公开的意见》答记者问</a><span class="new">
    href_list = re.findall('<a href="(.*?)" target="_blank" class="main">(.*?)</a></td><td width="80" align="right">(.*?)</td>',str(tab))

    for i in range(len(href_list)):
        date = href_list[i][-1]
        href = 'http://www.gdstc.gov.cn'+href_list[i][0]
        down_href = href.rstrip(href.split('/')[-1])
        title = href_list[i][1]
        # print(href,title,date)
        if re.findall('2018-04-04',date):
            html = getHtml(href)
            print(href)
            down_names = download(html,down_href)
            saveHtml(title, html)
            print("下载成功")

            # 向excel表插入超链接
            i = 0
            content = [title, "", source[i], date, href,""]
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
workbook.save('政府政策公告信息.xls')