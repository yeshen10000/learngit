import requests
from bs4 import BeautifulSoup

def getHtml(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
		r = requests.get(url,headers = headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None
def getIp(html):
	ip = []
	soup = BeautifulSoup(html,'html.parser')
	results = soup.find_all('tr',attrs = {'class':True})
	for result in results:
		if result('td'):
			print(result('td')[1].getText())


url = 'http://www.xicidaili.com/'
html = getHtml(url)
ip = []
getIp(html)
