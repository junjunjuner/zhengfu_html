from selenium import webdriver
import requests
import re
import time
import chardet
import urllib.request
from bs4 import BeautifulSoup as beautiful
import xlwt


#国家科技部


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}
#获取动态网页源码,参数为分页面url
def getHtml_move(url):
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome('/home/260199/chrome/chromedriver', chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    time.sleep(3)
    html_str = driver.page_source
    driver.quit()
    # html = urllib.request.urlopen(url).read()
    html = bytes(html_str, encoding="utf8")        #转码
    return html,html_str

#获取静态网页源码,参数为分页面url
def getHtml_quiet(url):
    html = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(html)
    chard = chardit1['encoding']
    html_req = requests.get(url)
    html_req.encoding = chard
    html_str = html_req.text
    return html,chard,html_str

#获取正文标题、附件信息，并下载附件，参数为分页面url，网页编码格式
def get_ctitle(html_str):
    bsObj = beautiful(html_str, "html.parser")
    #获取正文标题
    try:
        ctitle = bsObj.find('h1', {'id': 'con_title'}).text
    except:
        try:
            ctitle = bsObj.find('span', {'class': 'titleFont'}).text
        except:
            ctitle = None
    #获取附件信息,并下载
    file_infos = bsObj.find_all("a", {"href": re.compile(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$')})
    f = re.compile('<a href="(.*?)" target="_blank">(.*?)</a>')
    file_names = []
    for each in file_infos:
        # file_href = each['href']
        # print(file_info)
        file_info = re.findall(f, str(each))[0]
        print(file_info)
        file_href = file_info[0]
        if re.findall('http',file_href):
            pass
        else:
            file_href ='http://www.miit.gov.cn/' + file_href.split('../')[-1]
        print(file_href)
        file_loc = '/home/260199/政府政策公告信息/超链接/' + file_info[1]
        download_file(file_href,file_loc)
        file_names.append(file_info[1])
    return ctitle,file_names

#获取附件信息
def get_file(html_str):
    bsObj = beautiful(html_str, "html.parser")
    #获取附件信息,并下载
    file_infos = bsObj.find_all("a", {"href": re.compile(r'.doc$|.docx$|.pdf$|.xls$|.xlsx$')})
    file_names = []
    for each in file_infos:
        file_href = each['href']
        file_adds = file_href.split('.')[-1]
        file_name = each.text
        if re.findall(file_adds,file_name):
            pass
        else:
            file_name = file_name + '.' + file_adds
        if re.findall('http',file_href):
            pass
        else:
            file_href ='http://www.miit.gov.cn/' + file_href.split('../')[-1]
        print(file_href,file_name)
        file_loc = '/home/260199/政府政策公告信息/超链接/' + file_name
        download_file(file_href,file_loc)
        file_names.append(file_name)
    return file_names

#保存为html文件，并获取保存后的html文件全称（**.html）
def saveHtml(html_save, html_content):
    #    注意windows文件命名的禁用符，比如 /
    html_name = '/home/260199/政府政策公告信息/超链接/'+html_save.replace('/', '_') + ".html"
    with open(html_name, "wb") as f:
        #   写文件用bytes而不是str，所以要转码
        f.write(html_content)
    return html_name


#保存附件
def download_file(file_href,file_loc):
    r = requests.get(file_href, stream=True, headers=headers)
    # download started
    with open(file_loc, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

# 保存到excel表
def save_excel(worksheet, row, title,ctitle, html_name, source, date, complete_href, file_names):
    # 写入一行
    i = 0
    content = [ctitle, "", source, date, complete_href, ""]
    for each_header in content:
        worksheet.write(row, i, each_header)
        i += 1
    # 向excel表插入html文件超链接
    link = 'HYPERLINK("%s";"%s")' % (html_name, str(title))
    worksheet.write(row, 1, xlwt.Formula(link))
    # 向excel表插入附件超链接
    x = 5
    for down_name in file_names:
        print(down_name)
        file_loc = '/home/260199/政府政策公告信息/超链接/' + down_name
        link = 'HYPERLINK("%s";"%s")' % (file_loc, down_name)
        worksheet.write(row, x, xlwt.Formula(link))
        x = x + 1
        # worksheet.write(row, 1, xlwt.Formula('HYPERLINK("xx.html";title)'))  # Outputs the text "Google" linking to http://www.google.com

#国家工信部文件公示    静态网页
def wjgs_url(row,worksheet,url):
    source = '国家工信部文件公示'
    req = requests.get(url)
    #获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    #获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    li_list = soup.find_all('li')
    for li in li_list:
        li = str(li).replace('\n', '').replace('\r', '')
        print(li)
        a = re.compile('<a href="(.*?)" target="_blank">(.*?)</a><span><a href="../../../(.*?)" target="_blank">(.*?)</a></span></li>')
        info_list = re.findall(a, li)[0]
        print(info_list)
        #获取标题（在主页面显示的）
        title = info_list[1]
        #获取分页面url
        href = info_list[2]
        complete_href = 'http://www.miit.gov.cn/' + href
        #获取发布时间
        date = info_list[-1]
        #获取动态网页源码
        html,html_str = getHtml_move(complete_href)
        #保存为html文件
        html_name = saveHtml(title, html)
        #获取完整标题，附件（在分页面获取的）
        ctitle,file_names = get_ctitle(html_str)
        # 保存到excel表
        save_excel(worksheet, row, title,ctitle, html_name, source, date, complete_href, file_names)
        row = row + 1
    return row

#国家工信部文件发布   动态加载
def wjfb_url(row,worksheet,url):
    source = '国家工信部文件发布'
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    driver = webdriver.Chrome('/home/260199/chrome/chromedriver', chrome_options=options)
    driver.maximize_window()
    driver.get(url)
    js = "var q=document.documentElement.scrollTop=10000"
    driver.execute_script(js)
    time.sleep(5)
    tbody = driver.find_element_by_xpath(".//tbody[@id = 'contentBody']")
    trs = tbody.find_elements_by_xpath("./tr")
    # print(tbody)
    for tr in trs:
        ele_a = tr.find_element_by_tag_name('a')
        #获取分页面链接
        complete_href = ele_a.get_attribute('href')
        #获取正文标题
        title = ele_a.text
        #获取发布日期
        date = tr.find_element_by_xpath('td[5]').text
        #获取动态网页源码
        html, html_str = getHtml_move(complete_href)
        # 保存为html文件
        html_name = saveHtml(title, html)
        #获取附件（在分页面获取的）
        file_names = get_file(html_str)
        # 保存到excel表
        save_excel(worksheet, row, title,title, html_name, source, date, complete_href, file_names)
        row = row + 1
    driver.quit()
    return row

#国家工信部政策解读   静态加载
def zcjd_url(row,worksheet,url):
    source = '国家工信部政策解读'
    req = requests.get(url)
    # 获取网页编码格式
    response = urllib.request.urlopen(url).read()
    chardit1 = chardet.detect(response)
    chardit = chardit1['encoding']
    print("编码格式" + chardit)
    # 获取分页面url
    req.encoding = chardit1['encoding']
    soup = beautiful(req.text, 'lxml')
    lis = soup.find_all('li')
    for li in lis:
        a = li.find('a')
        href = a['href']
        complete_href = 'http://www.miit.gov.cn/' + href.split('../')[-1]
        title = a.text
        span = li.find('span')
        date = span.text
        html, chard, html_str = getHtml_quiet(complete_href)
        html_name = saveHtml(title, html)
        ctitle, file_names = get_ctitle(html_str)
        save_excel(worksheet, row, title, ctitle, html_name, source, date, complete_href, file_names)
        row = row + 1
    return row



def main():
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('科技部', cell_overwrite_ok=True)
    header = [u'标题', u'正文', u'政策来源处', u'发布日期', u'政策链接', u'附件']
    i = 0
    # 写表头
    for each_header in header:
        worksheet.write(0, i, each_header)
        i += 1
    row = 1
    # url1 = 'http://www.miit.gov.cn/n1146295/n1652858/n1653100/index.html'
    # row = wjgs_url(row, worksheet, url1)
    # print(row)
    # url2 = 'http://xxgk.miit.gov.cn/gdnps/wjfbindex.jsp'
    # row = wjfb_url(row, worksheet, url2)
    url3 = 'http://www.miit.gov.cn/n1146295/n1652858/n1653018/index.html'
    row = zcjd_url(row,worksheet,url3)
    print(row)
    workbook.save("/home/260199/政府政策公告信息/政府政策公告.xlsx")


if __name__ == '__main__':
    main()






