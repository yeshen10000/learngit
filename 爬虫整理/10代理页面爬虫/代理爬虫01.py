import requests
from bs4 import BeautifulSoup

ulist = []
url = 'http://www.xicidaili.com/nn/'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}

r = requests.get(url,headers = headers, timeout = 30)

soup = BeautifulSoup(r.text,'html.parser')

results = soup.find_all('tr',attrs = {'class':True})#得到的是一个结果集
for result in results:
	tds = result('td')

	test_url = 'http://ip.chinaz.com/getip.aspx'
	http = tds[1].string.strip()
	socket = tds[2].string.strip()
	h = tds[5].string.lower().strip()
	https = http+':'+socket
	proxy = {h:https}
	try:
		r = requests.get(test_url,headers = headers,proxies= proxy).status_code
		if r == 200:
			with open('daili.txt','a') as f:
				f.write(h+':'+https+'\n')
			print(h+https)
	except:
		print('useless')

	ulist.append([tds[1].string,tds[2].string,tds[3].get_text().strip(),tds[4].string,tds[5].string,tds[6]('div')[0]['title'],tds[7]('div')[0]['title'],tds[8].string,tds[9].string])
	"""
	对于BeautifulSoup通过find_all函数得到的结果集，用string得到的是直接节点的text内容，get_text()得到的是所有子孙节点中的内容；
	用（‘’）得到节点的子节点，['']能得到相应的属性值，如tds[6]('div')[0]['title']表示的是tr标签下第七个td标签下第一个div标签的title属性值

	"""
# for i in ulist:

	# print(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])