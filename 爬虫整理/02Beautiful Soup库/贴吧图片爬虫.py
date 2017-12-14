import requests
from bs4 import BeautifulSoup
import os
#获取html
f = requests.get('http://tieba.baidu.com/p/2166231880').text
#用BS解析html
s = BeautifulSoup(f,'lxml')
s_imgs = s.find_all('img',pic_type='0')
#逐个将图片保存到本地
i=1
os.mkdir("picture")
os.chdir("picture")
for s_img in s_imgs:
    img_url = s_img['src']
    img_content = requests.get(img_url).content
    file_name = str(i) + '.jpg'
    with open(os.getcwd()+'/'+file_name, 'wb') as wf:
        wf.write(img_content)
    i += 1
