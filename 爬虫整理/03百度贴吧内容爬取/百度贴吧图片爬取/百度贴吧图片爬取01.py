"""
查找的是对应贴吧中的图片，不包括头像图片

"""

import requests
import os
from bs4 import BeautifulSoup

def getHTML(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def downloadImg(html):
    os.mkdir("picture")
    os.chdir("picture")
    imgs=[]

    soup = BeautifulSoup(html,"html.parser")

    for img in soup.find_all('img',attrs={"class":"BDE_Image"}):
        imgs.append(img)

    i=1
    try:
        for simg in imgs:
            
            img_url = simg["src"]
            img_content = requests.get(img_url).content
    
            file_name = str(i) +'.jpg'
            with open(os.getcwd()+'/'+file_name,'wb') as f:
                f.write(img_content)
            i+=1
    except:
        print("wrong")

def main():
    url='https://tieba.baidu.com/p/5139272516'
    html=getHTML(url)
    downloadImg(html)
    print("success")

main()
        
    
