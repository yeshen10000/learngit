import requests
from bs4 import BeautifulSoup
import re
from urllib import parse
import os
import shutil
#获得对应的音乐的xml页面
def geturllist(url):
	urllist = []
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
	try:
		r = requests.get(url,headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		html = r.text
	except:
		print('wrong')
		html = None

	soup = BeautifulSoup(html,'html.parser')
	results = soup.find_all('tr',attrs={'class':True,'data-needpay':True,'data-playstatus':True,'data-downloadstatus':True,'data-json':True})

	for result in results:

		ids = result('input')[0]['value']
		urllist.append('http://www.xiami.com/song/playlist/id/'+ids+'/object_name/default/object_id/0')#这个格式是在网上找的，改变对应的id就能得到对应的音乐，http://blog.csdn.net/jrn1012/article/details/45747787可以参考

	return urllist


def downloadmusic(urllist,songname):
	j = 1
	if os.path.exists(songname):
		shutil.rmtree(songname)
		os.mkdir(songname)
	else:
		os.mkdir(songname)
	os.chdir(songname)
	for url in urllist:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}

		html = requests.get(url,headers=headers).text

		pattern_songName = re.compile(r'<songName>(.*?)</songName>')
		songName = re.search(pattern_songName,html).group(1).strip()
		if '?' in songName:
			songName = songName.replace('?','1')

		pattern_location = re.compile('<location>(.*?)</location>')
		location = re.search(pattern_location,html).group(1).strip()#这是音乐的加密后的url地址,通过凯撒阵列的方式进行加密的

		strlen = len(location[1:])
		rows = int(location[0])
		cols = strlen//rows
		right_rows = strlen%rows
		new_str = location[1:]
		url_true = ''
		for i in range(strlen):
			x = i%rows
			y = i/rows
			p = 0
			if x<=right_rows:
				p = x*(cols+1)+y
			else:
				p = right_rows*(cols+1)+(x-right_rows)*cols+y
			url_true+=new_str[int(p)]
		urlquote = parse.unquote(url_true)#编码问题，当发现这个字符串中有很多%而且看不明白，很有可能就是被quote了，只需要进行一下unquote就可以了，有时候可能还需要在参数中注明一下是utf-8还是gbk什么的编码
		urlmusic = urlquote.replace('^','0')#用0来替换里面的^符号

		music_content = requests.get(urlmusic).content
		music_name = songName+str(j)+'.mp3'

		with open(music_name,'wb') as f:
			f.write(music_content)

		print('第'+str(j)+'首歌下载完毕')
		j+=1




starturl = 'http://www.xiami.com/'

# songname = input('please input songname:')
songname = '冰雨'
url = starturl+'search?key='+songname+'&pos=1'
geturllist(url)
downloadmusic(geturllist(url),songname)

