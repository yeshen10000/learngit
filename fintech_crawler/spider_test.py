# encoding: utf-8
from news_feed.cn_stock import CNStock
from news_feed.cs_stock import CSStock
from news_feed.stcn_stock import STCNStock
from news_feed.cc_stock import CCStock
from news_feed.jingji21_stock import JingJi21Stock
from news_feed.p5w_stock import P5WStock
from news_feed.wabei_stock import WaBeiStock
from news_feed.chinaipo_stock import ChinaIpoStock
from news_feed.finance_sina import FinaceSina
import sys
import requests
from news_feed.we_chart import WeChart

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":

    temp = CNStock()
    # url = "https://mp.weixin.qq.com/s?timestamp=1512451356&src=3&ver=1&signature=V63EnHTNFNiNGk4fsxxqcwgU1c37GXpXFOEn0sfGkRfZM*2YhzOuRhyUemgLYZ1172YDvPwQ1GUgZtNeWBZDrEKREqv-Jskbbh0rZ5hLnBiNL-C3GzketwbM3irzDdCSfz*4UtVCqztB1lwMg2n0cPoH771yKeobWUhXxP**XSM="
    url = "http://irm.cnstock.com/content_company/index/000516/gsfb/826"
    # url = "https://www.newrank.cn/xdnphb/detail/getAccountArticle"
    # url = "https://www.newrank.cn/public/info/detail.html?account=yigoonet"
    # url = "http://www.chinaipo.com/news/"
    # url = "http://stock.cnstock.com/live"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        # "Host": "www.chinaipo.com"
    }
    # response = requests.post(url, headers=header, data={"uuid": "170407ABD4B63346CC220F9DEBC5A4D6",
    #                                                     "nonce": "d6fbeef8c", "flag": True, "xyz": "4660c266e73ca4e6030b7558e5c1bcb"})
    response = requests.get(url=url, headers=header)
    data = response.content.decode("utf-8")
    print data
    params = {
        "info:url": url,
        "info:priority": "99",
        "info:parse_func": "CNStock",
        "html": data
    }
    # # print '#', params
    content = temp.parse_content(data, params)
    print content
    # if content:
    #      import json
    #      hdfs.save(json.dumps(content))
    # print content
