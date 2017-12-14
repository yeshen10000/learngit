import requests
import re


def getHtml(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
		r = requests.get(url,headers = headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding

		return r.text
	except:
		print(r.status_code)
		return None

def getContent(html):
	pass

def main():
	base_url = 'http://www.xicidaili.com/nn/'
	print("start")

	i = 1

	url = base_url + str(i)


	while getHtml(url):
		#getContent(getHtml(url))
		print(i)
		i+= 1
		url = base_url + str(i)
		

main()