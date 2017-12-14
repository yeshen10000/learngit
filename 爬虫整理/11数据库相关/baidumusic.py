import pymysql
#import pymysql.cursors
import codecs

connect = pymysql.Connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='songyue',
	db='test',
	charset='utf8')

cursor = connect.cursor()#获取游标


cursor.execute('use test')
cursor.execute('drop table if exists baidumusic')
sql = 'create table baidumusic(id int auto_increment,songname varchar(50),singers varchar(50),album varchar(500),tagname varchar(50),songtype_auther varchar(50),typename varchar(50),url varchar(50),primary key(id))'
cursor.execute(sql)
connect.commit()
alist = []
for line in codecs.open('baidumusic.txt','r','UTF-8')：
	line = line.strip()
	a = line.split('\t')
	songname = a[0]
	singers = a[1]
	album = a[2]
	tagname = a[3]
	songtype_auther = a[4]
	typename = a[5]
	url = a[6]
	alist.append((songname,singers,album,tagname,songtype_auther,typename,url))

sql = "insert into baidumusic (songname,singers,album,tagname,songtype_auther,typename,url) values (%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,alist)#这是将所有的信息直接一次性插入，下面注释的是将所有的信息一条一条插入
	# sql = "insert into baidumusic (songname,singers,album,tagname,songtype_auther,typename,url) values (%s,%s,%s,%s,%s,%s,%s)"
	# data = (songname,singers,album,tagname,songtype_auther,typename,url)
	# print(data)
	# cursor.execute(sql,data)
	# connect.commit()
connect.commit()
cursor.close()
connect.close()
print('over')
