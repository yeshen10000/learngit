import pymysql
#import pymysql.cursors

connect = pymysql.Connect(
	host='localhost',
	port=3306,
	user='root',
	passwd='songyue',
	db='test',
	charset='utf8')

cursor = connect.cursor()#获取游标

# sql = 'insert into student (id,name,course) values (9,"zhang","chinese")'
# cursor.execute(sql)
# connect.commit()
# print('success'+str(cursor.rowcount))

sql = 'select name from student where name="zhang"'
cursor.execute(sql)
for row in cursor.fetchall():
	print('name:%s' %row)
print(cursor.rowcount)

sql = 'delete from student where id=%d'
data = (3,)
try:
	cursor.execute(sql %data)
	connect.commit()
	print(cursor.rowcount)
except:
	connect.rollback()#对数据进行修改之后应当try 一下，防止发生错误

cursor.close()
connect.close()
