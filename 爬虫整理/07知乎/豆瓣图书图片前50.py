import requests
from bs4 import BeautifulSoup
import os

def getHtml(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
		r = requests.get(url,headers = headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None

url = 'https://book.douban.com/top250?start=0'
html = getHtml(url)

soup = BeautifulSoup(html,'html.parser')
results = soup.find_all('img',attrs = {'src':True,'width':True})

if os.path.exists('pic'):
	os.chdir('pic')
else:
	os.mkdir('pic')
	os.chdir('pic')
i = 1
for result in results:
	if result['src']:
		content = requests.get(result['src']).content
		filename = str(i)+'.jpg'
		with open(os.getcwd()+'/'+filename,'wb') as f:
			f.write(content)
		i+=1
		print(i)