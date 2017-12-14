import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib import parse

def get_cookies(url):
	driver = webdriver.Firefox()
	driver.get('https://bbs.byr.cn/index')
	elem_user = driver.find_element_by_id('id')
	elem_user.send_keys('yeshen10000')
	time.sleep(1)
	ele_pw = driver.find_element_by_id('pwd')
	ele_pw.send_keys('19941210songyue')
	time.sleep(1)
	ele_pw.send_keys(Keys.RETURN)
	time.sleep(2)
	print(driver.current_url)
	cookielist = driver.get_cookies()
	# print(cookielist)
	cookie_dic = {}
	for cookie in cookielist:
		if 'name' in cookie and 'value' in cookie:
			cookie_dic[cookie['name']]=parse.unquote(cookie['value'])
	# print(cookie_dic)
	return cookie_dic

def get_html(url,cookie):#使用的是cookies登录
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
			   'X-Requested-With': 'XMLHttpRequest'}
	print(cookie)
	url = 'https://bbs.byr.cn/default?_uid='+cookie['login-user']
	try:
		session = requests.Session()
		r = session.get(url,headers=headers,cookies=cookie)
		# cook = requests.utils.dict_from_cookiejar(session.cookies)
		# print(cook)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text,session
	except:
		return None

def gettop10(html,session):
	urllist = []
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
			   'X-Requested-With': 'XMLHttpRequest'}
	soup = BeautifulSoup(html,'html.parser')
	results = soup.find_all('li',attrs={'id':'topten'})[0]
	soup1 = BeautifulSoup(str(results),'html.parser')
	results1 = soup1.find_all('li',attrs={'title':True})
	for result in results1:
		urllist.append([result('a')[0].get_text(),'https://bbs.byr.cn'+result('a')[0]['href']+'?_uid=yeshen10000'])
	return urllist

def main():
	url = 'https://bbs.byr.cn/index'
	cookie_dic = {}
	cookie_dic = get_cookies(url)
	html,session = get_html(url,cookie_dic)
	# get_top10url(html)
	urllist = []
	urllist = gettop10(html,session)
	for i in urllist:
		print(i)



main()
