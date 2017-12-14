import pymysql

connect = pymysql.Connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='songyue',
	db='test',
	charset='utf8')

cursor = connect.cursor()#获取游标
cursor.execute('use test')
sql = 'select distinct(stuid) from bupt order by stuid desc'
cursor.execute(sql)
for i in cursor.fetchall():
	print(i[0])
print(cursor.rowcount)

cursor.close()
connect.close()