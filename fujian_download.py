from bs4 import BeautifulSoup as bf
import re
import requests
url = 'http://www.gdcom.gov.cn/zwgk/gggs/201803/t20180328_159194.html'
req = requests.get(url).text
soup = bf(req,'lxml')
a = soup.find_all(class_='pdf')
print(a)
