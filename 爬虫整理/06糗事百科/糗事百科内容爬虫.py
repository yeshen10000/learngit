import requests
import re
import os
from bs4 import BeautifulSoup


"""
这段代码师对糗事百科首页的段子进行爬虫，注意get_text()函数
url = "http://www.qiushibaike.com/"
html = requests.get(url).text

soup = BeautifulSoup(html,"html.parser")

results = soup.find_all("div", "content")

cont = []
for result in results:
	cont.append(result.get_text())#get_text()函数表示的是取到Tag标签的所有文本内容

i = 1
for c in cont:
	print('No %d duanzi:',i)
	print(c)
	print('---------------------------------\n')
	i = i+1


"""




"""
这段代码是用来爬糗事百科评论的内容
url = "http://www.qiushibaike.com/article/118776539"
html = requests.get(url).text

soup = BeautifulSoup(html,"html.parser")

results = soup.find_all("div","replay")

for i in results:
	print(i.span.string)
"""