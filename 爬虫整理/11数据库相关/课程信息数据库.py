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

cursor.execute('use test')
cursor.execute('drop table if exists bupt')
sql = 'create table bupt(courseNo char(10) not null,coursename varchar(50),classname varchar(50),courseinfo varchar(200),stuid char(10) not null,stuname varchar(10),stusex char(4),studep char(4),primary key(courseNo,stuid))'
cursor.execute(sql)
connect.commit()
alist = []
for line in open('bupt.txt'):
	line = line.strip()
	a = line.split('\t')
	courseNo = a[0]
	coursename = a[1]
	classname = a[2]
	courseinfo = a[3]
	stuid = a[4]
	stuname = a[5]
	stusex = a[6]
	studep = a[7]
	alist.append((courseNo,coursename,classname,courseinfo,stuid,stuname,stusex,studep))

sql = "insert into bupt (courseNo,coursename,classname,courseinfo,stuid,stuname,stusex,studep) values (%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql,alist)#这是将所有的信息直接一次性插入，下面注释的是将所有的信息一条一条插入
	# sql = "insert into bupt (courseNo,coursename,classname,courseinfo,stuid,stuname,stusex,studep) values (%s,%s,%s,%s,%s,%s,%s,%s)"
	# data = (courseNo,coursename,classname,courseinfo,stuid,stuname,stusex,studep)
	# print(data)
	# cursor.execute(sql,data)
	# connect.commit()
connect.commit()
cursor.close()
connect.close()
print('over')
