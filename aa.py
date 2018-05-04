import requests
import urllib.request
import chardet
import re
from bs4 import BeautifulSoup as beautiful
from selenium import webdriver
import time

# start_url = 'http://www.miit.gov.cn/n1146295/n1652858/n1653100/index.html'
# req = requests.get(start_url)
# response = urllib.request.urlopen(start_url).read()
# chardit1 = chardet.detect(response)
# print("编码格式" + chardit1['encoding'])
# req.encoding = chardit1['encoding']
# #以下方式匹配太宽泛
# # a = re.compile(r'<a href=(.*?) target=_blank>(.*?)</a>(.*?)<span><a href=../../../(.*?) target=_blank>(.*?)</a></span>',re.S)
#
# soup = beautiful(req.text,'lxml')
# li_list = soup.find_all('li')
# for li in li_list:
#     li = str(li).replace('\n','').replace('\r','')
#     print(li)
#     a = re.compile('<a href="(.*?)" target="_blank">(.*?)</a><span><a href="../../../(.*?)" target="_blank">(.*?)</a></span></li>')
#     info_list = re.findall(a,li)
#     print(info_list)



# url = 'http://zmhd.miit.gov.cn:8080/opinion/noticedetail.do?method=notice_detail_show&noticeid=1901'
# chard = 'utf-8'
# driver = webdriver.Chrome('/home/260199/chrome/chromedriver')
# driver.get(url)
# js = "var q=document.documentElement.scrollTop=10000"
# driver.execute_script(js)
# time.sleep(3)
# html_str = driver.page_source
# # req.encoding = chard
# # # 获取正文标题
# # a = re.compile('<div class="ctitle"><h1  id="con_title" style="line-height: 40px; padding:0 120px;">(.*?)</h1></div>')
# # ctitle = re.findall(a, req.text)
# # print(ctitle)
# bsObj = beautiful(html_str, "html.parser")
# try:
#     ctitle = bsObj.find('h1',{'id':'con_title'}).text
# except:
#     try:
#         ctitle = bsObj.find('span', {'class': 'titleFont'}).text
#     except:
#         ctitle=None
# print(ctitle)
# pdfs = bsObj.find_all("a", {"href": re.compile(r'.doc$|.docx$')})
# f = re.compile('<a href="(.*?)" target="_blank">(.*?)</a>')
# # f = re.compile('<a href="(.*?)" target="_blank">(.*?)</a>')
# for each in pdfs:
#     file_info = re.findall(f, str(each))
#     print(file_info)
# driver.quit()

# url = 'http://xxgk.miit.gov.cn/gdnps/wjfbindex.jsp'
# options = webdriver.ChromeOptions()
# options.add_argument('disable-infobars')
# driver = webdriver.Chrome('/home/260199/chrome/chromedriver',chrome_options=options)
# driver.maximize_window()
# driver.get(url)
# js = "var q=document.documentElement.scrollTop=10000"
# driver.execute_script(js)
# time.sleep(3)
# tbody = driver.find_element_by_xpath(".//tbody[@id = 'contentBody']")
# trs = tbody.find_elements_by_xpath("./tr")
# # print(tbody)
# for tr in trs:
#     # tex = t.text
#     # try:
#     #     # print(t.get_attribute("innerHTML"))
#     #     soup = beautiful(t.get_attribute("innerHTML"),'lxml')
#     #     a = soup.find('a',attrs={'href':True})
#     #     print(a['href'])
#     #     print(soup)
#     #     # break
#     # except Exception as e:
#     #     print(e)
#     #     driver.quit()
#     #     break
#     # tt = t.find_element_by_xpath(".//td[2]/a")
#     # print(tt)
#     ele_a = tr.find_element_by_tag_name('a')
#     complete_href = ele_a.get_attribute('href')
#     title = ele_a.text
#     print(complete_href,title)
#     date = tr.find_element_by_xpath('td[5]').text
#     print(date)
# # tr_list = tbody.find_elements_by_tag_name('tr')
# # for tr in tr_list:
# #     t = tr.find_element_by_tag_name('a').text
# #     print(t)
#
# if driver:
#     driver.quit()
url = 'http://www.mohurd.gov.cn/wjfb/index.html'
source = '国家住建部政策发布'
req = requests.get(url)
# 获取网页编码格式
response = urllib.request.urlopen(url).read()
chardit1 = chardet.detect(response)
chardit = chardit1['encoding']
print("编码格式" + chardit)
# 获取分页面url
req.encoding = chardit1['encoding']
soup = beautiful(req.text, 'lxml')
item_list = soup.find_all('td',{'style':'text-align:left;'})
date_list = soup.find_all('td',{'style':'width:86px;text-align:left; color:#ABABAB;'})
for i in range(len(item_list)):
    item = str(item_list[i])
    complete_href = re.findall('<a href="(.*?)"',item)[0]
    title = re.findall('>(.*?)</a>',item)[0]
    date = re.findall('>\[(.*?)\]</td>',str(date_list[i]))[0]
    print(complete_href,title,date)
# alitem_list=soup.find_all('tr',{'class':'alitem'})
# al_list = item_list + alitem_list
# print(len(al_list))
# for al in al_list:
#     al = str(al).replace('\n', '').replace('\r', '')
#     print(al)
#     complete_href = re.findall('<a href="(.*?)" message=', al)[0]
#     ctitle = re.findall('&amp;&amp;(.*?)" onmousemove=',al)[0].replace('&amp;','')
#     title = re.findall('target="_blank">(.*?)</a>',al)[0]
#     date = re.findall('<td>(.*?)</td>',al)[0]
#     print(complete_href)
#     print(ctitle)
#     print(title,date)
# #<a href='http://www.mohurd.gov.cn/wjfb/201804/t20180425_235829.html' target='_blank' message='000013338/2018-00107&城市建设&中华人民共和国住房和城乡建设部办公厅&2018-04-20&建办城函[2018]207号&&住房城乡建设部办公厅关于做好2018年全国城市节约用水宣传周工作的通知' onmouseover='showTooltip(this,event);' onmousemove='Locate(event);' onmouseout='hideTooltip(event);'>住房城乡建设部办公厅关于做好2018年全国城市节约用水...</a>


# print(lis)