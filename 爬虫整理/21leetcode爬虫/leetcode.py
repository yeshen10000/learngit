import requests
from bs4 import BeautifulSoup
import json
import pymysql


def get_Html(url):
	try:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
		r = requests.get(url,headers = headers)
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return None

def get_Description(url):
	html = get_Html(url)
	soup = BeautifulSoup(html,'html.parser')
	des = soup.find('p').get_text()
	return des





def get_Title(html):
	connect = pymysql.Connect(
		host='localhost',
		port=3306,
		user='root',
		passwd='songyue',
		db='test',
		charset='utf8')

	cursor = connect.cursor()  # 获取游标

	cursor.execute('use test')
	cursor.execute('drop table if exists leetcode')
	sql = 'create table leetcode(id varchar(10) not null,title varchar(500),difficulty VARCHAR(4),url varchar(200),description varchar(10000) not null,primary key(id))'
	cursor.execute(sql)
	connect.commit()

	dic = json.loads(html)
	# f = open('leetcode.txt','a',encoding = 'utf-8')
	for i in dic['stat_status_pairs']:
		title = i['stat']['question__title']
		id = str(i['stat']['question_id'])
		difficulty = str(i['difficulty']['level'])
		title_slug = i['stat']['question__title_slug']
		url = 'https://leetcode.com/problems/'+title_slug+'/description/'
		description = get_Description(url)
		# f.write(str(id)+'\t'+title+'\n'+description+'=================================================='+'\n'+"\n")
		sql = "insert into leetcode (id,title,difficulty,url,description) values (%s,%s,%s,%s,%s)"
		data = (id,title,difficulty,url,description)
		cursor.execute(sql,data)
		connect.commit()
		print(id)
	cursor.close()
	connect.close()
	# f.close()


def main():
	url = 'https://leetcode.com/api/problems/algorithms/'
	html = get_Html(url)
	get_Title(html)





main()