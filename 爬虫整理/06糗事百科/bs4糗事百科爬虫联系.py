import requests
from bs4 import BeautifulSoup
import os
import re

def getHtml(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
		r = requests.get(url,headers = headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None

#def getHeaderPic(html):
	soup = BeautifulSoup(html,'html.parser')
	results = soup.find_all('img',attrs = {'src':True,'alt':True})
	i = 1
	os.mkdir('head_pic')
	os.chdir('head_pic')
	for result in results:
		file_name = result['alt']+'.jpg'
		pic_url = 'http:' + result['src']
		with open(os.getcwd()+'/'+file_name,'wb') as f:
			f.write(requests.get(pic_url).content)

	
def getHeader(html):
	soup = BeautifulSoup(html,'html.parser')
	result = soup.find('div',attrs = {'class':'content'})
	return result.string.strip()

def getReview(html):
	soup = BeautifulSoup(html,'html.parser')
	i = soup.find('div',attrs ={'id':'comment-376518446','class':'comment-block clearfix floor-1'})

	results = soup.find_all('div',attrs = {'id':re.compile(r'comment-(.*?)'),'class':re.compile(r'comment-block clearfix floor-(\d{1,3})')})
	print(results)
	for result in results:
		div = result('div')
		floor = div[3].string.strip()
		name = div[1]('a')[0].get('title')
		content = div[1]('span')[0].string.strip()

		print("floor:"+floor)
		print('viewer:'+name)
		print('content:'+content)
		print('-----------------------------------------')



url = 'https://www.qiushibaike.com/article/119161052'
html = getHtml(url)
#getHeaderPic(html)
print('内容:'+getHeader(html)+'\n')
print('评论：'+'\n')
getReview(html)