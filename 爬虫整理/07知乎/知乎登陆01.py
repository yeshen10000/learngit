import requests  
from bs4 import BeautifulSoup  
import urllib  
import re  
import json

loginUrl = 'https://account.xiaomi.com/pass/serviceLoginAuth2?_dc=1497510699272'  
formData = {'id':'yeshen10000',
            'passwd':'19941210songyue',
            'mode':'0',
            'CookieDate':'0'
            }
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  

url = 'https://bbs.byr.cn/#!article/AimGraduate/1110671'
s = requests.get(url)
print(s.text)
