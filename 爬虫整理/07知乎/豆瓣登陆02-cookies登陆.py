import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib import parse
def get_cookies(url):
	driver = webdriver.Firefox()
	driver.get(url)
	time.sleep(2)
	elem_user = driver.find_element_by_id('email')
	elem_user.clear()
	elem_user.send_keys('13051256262')
	ele_pw = driver.find_element_by_id('password')
	ele_pw.send_keys('19941210songyue')
	ele_pw.send_keys(Keys.RETURN)
	time.sleep(3)
	cookielist = driver.get_cookies()
	cookie_dic = {}
	for cookie in cookielist:
		if 'name' in cookie and 'value' in cookie:
			cookie_dic[cookie['name']]=parse.unquote(cookie['value'])
	print(cookie_dic)
	return cookie_dic
def get_html(url,cookie):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'}
	try:
		session = requests.session()
		url = 'https://www.douban.com/'
		print(session.get(url,headers=headers,cookies=cookie).text)
	except:
		print('hi')

def main():
	url = 'https://accounts.douban.com/login'
	cookie_dic = {}
	cookie_dic = get_cookies(url)
	get_html(url,cookie_dic)
	# cookieslogin(url)
main()
