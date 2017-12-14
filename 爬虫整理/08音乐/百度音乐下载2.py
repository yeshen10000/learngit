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
	soup = BeautifulSoup(html,"html.parser")
	results = soup.find_all("img")

	pattern = re.compile('<img.*?src="(.*?)".*?>',re.S)
	results2 = pattern.findall(html)

	i = 1
	os.mkdir("pic")
	os.chdir("pic")

	for result in results2:
			
		if(result!=""):
			if result[0]=='h':
				result = result
			elif result[1]=='/':
				result = 'http:'+result
			else:
				result = 'http:/'+result

			if result[7] == 's':#这里遇到的主要问题有：1有些result是空的，要去除；2对于地址是static的src获取不到资源，舍弃
				continue

			print("download %d:"%i)
			img_content = requests.get(result).content
			filename = str(i)+'.jpg'
			with open(os.getcwd()+'/'+filename,"wb") as f:
				f.write(img_content)

		i=i+1






url = 'http://music.baidu.com/'
downloadMusic(url)