#python爬取网页的通用代码框架

import requests #导入requests库

url = "http://www.baidu.com"#设置一个url地址
try:
    r = requests.get(url)#返回一个response对象
    r.raise_for_status()#如果返回状态是200，表示成功继续执行，否则跳进except
    r.encoding = r.apparent_encoding#获得备选编码
    print(r.text)#打印出来前1000个字符
except:             #利用try...except来避免产生的异常
    print("failed")

