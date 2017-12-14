# coding=utf-8
from pyquery import PyQuery
import urlparse
import os
import requests
import sys
import redis
import time
reload(sys)
sys.setdefaultencoding('utf8')


class WeChartSpider(object):

    base_file_path = "/home/abc/wechart_data/yiyao"
    start_urls = [
        "http://chuansong.me/account/yigoonet"
        # "http://chuansong.me/account/mycaijing",
        # "http://chuansong.me/account/cctvyscj",
        # "http://chuansong.me/account/sinacaijing",
        # "http://chuansong.me/account/i-caijing",
        # "http://chuansong.me/account/finance_ifeng",
        # "http://chuansong.me/account/Femorning",
        # # "http://chuansong.me/account/gdwscjly",
        # # "http://chuansong.me/account/BTV-tianxiacaijing",
        # "http://chuansong.me/account/kongfuf",
        # "http://chuansong.me/account/money-163",
        # "http://chuansong.me/account/p5w2012",
        # # "http://chuansong.me/account/souhucaijing2016",
        # # "http://chuansong.me/account/yazhoucaijing",
        # # "http://chuansong.me/account/ytcj123",
        # "http://chuansong.me/account/jjrbwx",
        # # "http://chuansong.me/account/TheEconomistGroup",
        # "http://chuansong.me/account/financeapp",
        # # "http://chuansong.me/account/jjzswx",
        # "http://chuansong.me/account/eeo-com-cn",
        # # "http://chuansong.me/account/ths518",
        # # "http://chuansong.me/account/xbxuelicai",
        # # "http://chuansong.me/account/caijinghui",
        # "http://chuansong.me/account/cbn-yicai",
        # # "http://chuansong.me/account/chuangtianxiahuodong",
        # "http://chuansong.me/account/wallstreetcn",
        # "http://chuansong.me/account/jjckb-wx",
        # "http://chuansong.me/account/davos_wef",
        # "http://chuansong.me/account/yicainews",
        # "http://chuansong.me/account/cctv2pinglun",
        # "http://chuansong.me/account/CBNweekly2008",
        # # "http://chuansong.me/account/icaijing88",
        # "http://chuansong.me/account/laohucaijing01",
        # "http://chuansong.me/account/cjtxzk",
        # "http://chuansong.me/account/cetnews",
        # "http://chuansong.me/account/ChinaEconomicWeekly",
        # "http://chuansong.me/account/jjbd21",
        # "http://chuansong.me/account/ccefccef",
        # # "http://chuansong.me/account/ifeng_fin_institute",
    ]
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Host": "chuansong.me",
        "Accept-Encoding": "gzip, deflate",
    }
    html_num = 0
    redis_action = redis.Redis()

    def get_pages(self, url):
        body = requests.get(url, headers=self.header).text
        dom = PyQuery(body)
        page = dom('div.w4_5 > span > a').eq(-1).text()
        self.page_to_redis(url, int(page))
        time.sleep(1)
        print page, url

    def page_to_redis(self, _url, page_nums):
        for i in range(page_nums):
            self.header["Referer"] = _url
            self.redis_action.rpush("yiyao_queue", _url + "?start={}".format(i*12))

    def parse_detail_url(self, detail_url):
        body = requests.get(detail_url, headers=self.header).text
        dom = PyQuery(body)
        for news in dom("a.question_link"):
            news_url = PyQuery(news).attr("href")
            ari_url = urlparse.urljoin("http://chuansong.me", news_url)
            self.download_html(ari_url)
        return dom("a.question_link")

    def download_html(self, download_url):
        body = requests.get(download_url, headers=self.header).text
        if body.find("503 Service Temporarily Unavailable") > -1:
            time.sleep(2)
            self.download_html(download_url)
        else:
            time.sleep(0.5)
            file_path = os.path.join(self.base_file_path, str(self.html_num/10000))
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            with open(file_path+"/%s.txt" % (str(self.html_num % 10000)), "w") as fp:
                fp.write(body)
                self.html_num += 1
            print download_url, "finished"


if __name__ == "__main__":
    temp = WeChartSpider()
    num = temp.html_num
    # for url in temp.start_urls:
    #     temp.get_pages(url)
    redis_action = redis.Redis()
    index = 0
    while redis_action.llen("yiyao_queue"):
        url = redis_action.lindex("yiyao_queue", 0)
        result = temp.parse_detail_url(url)
        # print url, result
        if result:
            redis_action.lpop("yiyao_queue")
        else:
            time.sleep(5)


