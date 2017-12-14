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


base_url = 'https://movie.douban.com/top250'
list = []
j = 1
for i in range(0,250,25):
	url = base_url + '?start=' + str(i) + '&filter='
	html = getHtml(url)
	soup = BeautifulSoup(html,'html.parser')

	resultss = soup.find('ol',attrs = {'class':'grid_view'})

	results = resultss.find_all('li')

	for result in results:
		
		name = result('a')[1]('span')[0].string
		score = result.find('span',attrs = {'class':'rating_num','property':'v:average'}).string
		people = result('div')[5]('span')[3].string

		list.append([name,score,people])
		
for l in list:
	print('{0:5}{1:>15}\t{2:>5}\t{3:>15}'.format(str(j),l[0],l[1],l[2]))
	j+=1







