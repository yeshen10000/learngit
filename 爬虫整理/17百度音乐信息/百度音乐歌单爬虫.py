import requests
from bs4 import BeautifulSoup
import codecs
import time

def get_url_text(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
	try:
		r = requests.get(url,headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None

def get_page_urllist(html):
	urllist = []
	soup = BeautifulSoup(html,'html.parser')
	page = int(soup.find('a',attrs={'class':'page-navigator-number PNNW-D '}).get_text())
	for i in range(page):
		url = 'http://music.baidu.com/songlist/tag/%E5%85%A8%E9%83%A8?orderType=1&offset='+str(i*20)+'&third_type='
		urllist.append(url)
	return urllist


def get_songtype_urllist(page_urllist):
	songtype_urllist = []
	i = 1
	for url in page_urllist:

		html = get_url_text(url)
		while html==None:
			time.sleep(5)
			print('wrong----------')
			html = get_url_text(url)
		
		soup = BeautifulSoup(html,'html.parser')
		results = soup.find_all('p',attrs={'class':'text-title'})
		for result in results:
			href = result('a')[0]['href']
			title = result('a')[0]['title']
			songtype_urllist.append([href,title])
			print(i)
			i+=1
	return songtype_urllist

def get_songinfo_list(songtype_urllist):
	f = codecs.open('baidumusic.txt','a','UTF-8')
	j=1
	k=1
	for i in songtype_urllist:
		print('No'+str(k)+'-----------------------')
		url = 'http://music.baidu.com'+ i[0]
		print(url)
		typename = i[1]

		html = get_url_text(url)
		while html==None:
			time.sleep(5)
			print('wrong============')
			html = get_url_text(url)

		soup = BeautifulSoup(html,'html.parser')

		try:

			songtype_auther = soup.find('a',attrs={'class':'songlist-info-username f16 pa'}).get_text().strip()
		except:
			print('==========================================================================================================')
			html = get_url_text(url)
			while html==None:
				time.sleep(5)
				print('wrong============')
				html = get_url_text(url)

			soup = BeautifulSoup(html,'html.parser')
			songtype_auther = soup.find('a',attrs={'class':'songlist-info-username f16 pa'}).get_text().strip()




		taglist = soup.find('div',attrs={'class':'songlist-info-tag'})
		tags = taglist('a')
		tagname = ''
		for tag in tags:
			tagname = tagname+' '+tag.get_text()

		results = soup.find_all('li',attrs={'data-songitem':True})
		for result in results:

			text = str(result)
			s = BeautifulSoup(text,'html.parser')
			songname = s.find('a',attrs={'href':True,'target':'_blank','title':True}).get_text().strip()
			singerlist = s.find_all('a',attrs={'hidefocus':'true','href':True})
			singers = ''
			for singer in singerlist:
				if singers=='':
					singers = singers+singer.get_text().strip()
				else:
					singers = singers+'/'+singer.get_text().strip()

			try:
				album = result('div')[0]('span')[-1]('a')[0]['title'].strip()
			except:
				album = ''
			print(str(j)+'===='+songname)
			j+=1
			f.write(songname+'\t'+singers+'\t'+album+'\t'+tagname+'\t'+songtype_auther+'\t'+typename+'\t'+url+'\n')
		k+=1

	f.close()
			

if __name__=='__main__':
	url = 'http://music.baidu.com/songlist/tag/%E5%85%A8%E9%83%A8?orderType=1&offset=0&third_type='
	html = get_url_text(url)
	pagelist = get_page_urllist(html)
	songtype_urllist = get_songtype_urllist(pagelist)
	get_songinfo_list(songtype_urllist)