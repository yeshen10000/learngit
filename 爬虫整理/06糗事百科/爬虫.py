"""
遇到的问题以及解决方法：
1.复制粘贴经常会遇到格式上的错误：
	重新换行就好

2.爬取图片的时候注意可能会有不同类型的图片：
	打印爬出爬出来的图片url地址，仔细观察一下之间的区别，注意有的图片url地址前面没有http:，要自己加上，主要注意url地址类型是http://格式，不一样的要自己加上

3.注意findall函数中的参数信息：
	可以加上多种限制调价，对pic_type不太了解

4.对正则表达式的使用还是不是熟练：
	正则得到的是字符串，find_all得到的是一个结果集，注意区别

"""



import requests
from bs4 import BeautifulSoup
import os
#获取html
f = requests.get('http://www.qiushibaike.com/').text
#用BS解析html
s = BeautifulSoup(f,'lxml')
s_imgs = s.find_all('img')
#逐个将图片保存到本地
print(type(s_imgs))
i=1
for s_img in s_imgs:
    img_url = s_img['src']
    print(img_url)
    if img_url[1] == '/':
    	img_url = 'http:' + img_url
    else:
    	continue
    img_content = requests.get(img_url).content
    file_name = str(i) + '.jpg'
    with open(os.getcwd()+'/'+file_name, 'wb') as wf:
        wf.write(img_content)
    i += 1