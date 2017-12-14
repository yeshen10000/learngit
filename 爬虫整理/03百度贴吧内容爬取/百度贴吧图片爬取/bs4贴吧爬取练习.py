import requests
from bs4 import BeautifulSoup
import os

def getHtml(url):
	try:
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"}
		r = requests.get(url,headers = headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None
#获取头像的函数
#def getHeaderPic(html):#注意网页是分步加载的，首先使用默认的头像展示，再逐步下载自定义头像替换，因此还要得到自定义头像的地址，所以在results结果中很多头像的地址是在data-tb-lazyload属性中的
	srclist = []
	if html:
		soup = BeautifulSoup(html,'html.parser')
		results = soup.find_all('img',attrs={'class':True,'username':True,'src':True})
		for result in results:
			if result.get('data-tb-lazyload'):#这句话是判断result这个tag中是否包含data-tb-lazyload这个属性！！！！
				if (result['data-tb-lazyload'],result['username']) in srclist:#判断是否在这个列表中已经存在了这个图片
					continue
				else:
					srclist.append((result['data-tb-lazyload'],result['username']))
			else:
				if (result['src'],result['username']) in srclist:
					continue
				else:
					srclist.append((result['src'],result['username']))

		os.mkdir('headerpic')
		os.chdir('headerpic')

		for pic in srclist:
			headpic_name = pic[1] + '.jpg'
			headpic_url = pic[0]
			with open(os.getcwd()+'/'+headpic_name,'wb') as f:
				f.write(requests.get(headpic_url).content)

	else:
		return None

#def getPic(html):
	if html:
		img_list = []
		soup = BeautifulSoup(html,'html.parser')
		results = soup.find_all('img',attrs ={'class':'BDE_Image','src':True})
		for result in results:
			img_list.append(result.get('src'))
		os.mkdir('pic')
		os.chdir('pic')
		
		

		for pic in img_list:
			filename = pic.split('/')[-1]
			pic_url = pic
			with open(os.getcwd()+'/'+filename,'wb') as f:
				f.write(requests.get(pic_url).content)
			




url = 'https://tieba.baidu.com/p/5158548640?pn='

#getHeaderPic(html)
#getPic(html)
