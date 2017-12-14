#CrawUnivRankingA.py
import requests
from bs4 import BeautifulSoup
import bs4
 
def getHTMLText(url):#从网络上获取大学排名网页内容
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""
 
def fillUnivList(ulist, html):#提取网页内容中的信息到合适的数据结构
    soup = BeautifulSoup(html, "html.parser")#利用beautifulsoup来将爬取的页面用html方式解析，得到一个标签树
    for tr in soup.find('tbody').children:#在html代码中可以观察得到，所有大学的信息在tbody中，每个大学的信息在tobody的tr中。
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')                      #将tr中的td信息存储进tds列表中
            ulist.append([tds[0].string, tds[1].string, tds[3].string])
 
def printUnivList(ulist, num):#利用数据结构展示并输出结果
    print("{:^10}\t{:^6}\t{:^10}".format("排名","学校名称","总分"))
    for i in range(num):
        u=ulist[i]
        print("{:^10}\t{:^6}\t{:^10}".format(u[0],u[1],u[2]))
     
def main():
    uinfo = []
    url = 'http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, 20) # 20 univs
main()
