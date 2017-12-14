import requests
from bs4 import BeautifulSoup
import re
import os

def getHtml(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
		response.encoding = response.apparent_encoding
		return response.text
	except:
		return ""


def downloadMusic(url):
	html = getHtml(url)
	pattern = re.compile(r'<div class="mod mod-song-rank js-mod mod-[^k].*?" monkey="(.*?)" data-js-mod-name="(.*?)">')
	#matches = pattern.findall(html)
	#for match in matches:
	#	print(match)
	soup = BeautifulSoup(html,"html.parser")

	data = soup.select('div.ranklist-wrapper.clearfix div.bd ul.song-list li')#有关select的含义见BeautifulSoup中的CSS选择器的txt文件的网址，注意这里的clearfix其实在院html代码中与前面是有空格的
	
	pattern1 = re.compile(r'<li.*?><div class="index">(.*?)</div>.*?<a.*?>(.*?)</a>.*?<a.*?>(.*?)</a>',re.S)

	wants = []

	for item in data:
		final = re.findall(pattern1,str(item))#final是一个列表,里面包含的是一个元组,所以用final.group(1)是错误的；但是如果这里是search函数，返回的是匹配对象，用group获取字符串，那么就可以用了
		wants.append(final[0])

	j=1
	for i in wants:
		print("序号:%-4s 歌手：%-20s 歌名：%-15s"%(i[0],i[1],i[2]))
		j+=1
	print(j)
	

url = 'http://music.baidu.com/'
downloadMusic(url)