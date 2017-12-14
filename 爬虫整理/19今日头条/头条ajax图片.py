import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json
import re
import os
import multiprocessing

j=1

def get_json(offset,keyword):
	data = {
		'offset':offset,
		'format':'json',
		'keyword':keyword,
		'autoload':'true',
		'count':'20',
		'cur_tab':'3'
	}
	url = 'http://www.toutiao.com/search_content/?'+urlencode(data)

	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print('json wrong========')
		return None


def get_json_url(html):
	data = json.loads(html)
	article_list = []

	if data and 'data' in data.keys():
		for i in data.get('data'):
			article_list.append(i.get('article_url'))
	return article_list

def get_article_html(url):
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		print('json wrong========')
		return None

def get_image_url(html):
	urllist = []
	pattern = re.compile('var gallery = (.*?);',re.S)
	results = pattern.search(html)
	if results:
		data = json.loads(results.group(1))
		if data and 'sub_images' in data.keys():
			sub_images = data.get('sub_images')
			for i in sub_images:
				urllist.append(i.get('url'))
	return urllist

def download_image(urllist):
	global j
	for url in urllist:
		image_content = requests.get(url).content
		filename = str(j)+'.jpg'
		with open(filename,'wb') as f:
			f.write(image_content)
		j+=1


def main():
	html = get_json(0,'野兽')
	article_list = []
	imageurl_list = []
	article_list = get_json_url(html)
	for i in article_list:
		h = get_article_html(i)
		imageurl_list = get_image_url(h)
		print(imageurl_list)
		download_image(imageurl_list)
	# pool = multiprocessing.Pool(multiprocessing.cpu_count())
	# for i in article_list:
	# 	# h = get_article_html(i)
		# imageurl_list = get_image_url(h)
		# print(imageurl_list)
		# pool.apply_async(download_image,(imageurl_list,))
		#pool.apply_async(download_image(get_image_url(get_article_html)),(i,))
	# pool.close()
	# pool.join()


if __name__ == '__main__':
	os.chdir('picture')
	main()


