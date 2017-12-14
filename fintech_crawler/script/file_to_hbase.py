# encoding: utf-8
import os
import sys
import urlparse
import traceback
import requests
import urllib2
import urllib
from pyquery import PyQuery
from datetime import datetime
sys.path.append("..")
from db_actions.hbase_action import HBASEAction
from db_actions.redis_action import RedisAction
from utilty.link_analysis import LinkExtractor
hbase_client = HBASEAction()
redis_client = RedisAction()


def parse_item(html):
    dom = PyQuery(html)
    store_json = {
        "info:title": dom("div#img-content > h2#activity-name").text(),
        "info:publish_time": dom("div.rich_media_meta_list > em#post-date").text(),
        "info:source": dom("a#post-user").text(),
        "info:author": dom("div.rich_media_meta_list > em").eq(1).text(),
        "info:content": LinkExtractor().strip_html5_whitespace(dom("div#page-content").html()),
        "info:tag": dom("div.model-tags > a").text(),
        "info:dese": "",
        "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "info:url": "",
        "info:channel": "wecharts",
        "info:laiyuan": "http://weixin.sogou.com/weixin",
        "info:contain_image": "True" if dom("div#page-content")("img") else "False"
    }
    return store_json


def get_source_url(title, source):
    url = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&ch=&tn=baiduhome_pg&bar=&wd={k}".format(k=urllib.quote("%s %s" % (source, title)))
    # print url
    html = urllib2.urlopen(url).read()
    return PyQuery(html)("div#1 > h3.t > a").attr("href")


if __name__ == "__main__":
    error = open("error.txt", 'a')

    for i in range(0, 10000):
        with open("/home/abc/wechart_data/1/{name}.txt".format(name=i), 'r') as fp:
            try:
                store_json = parse_item(fp.read().strip())
                store_json["info:url"] = get_source_url(store_json["info:title"].encode("utf-8"), store_json["info:source"].encode("utf-8"))
                url = requests.get(store_json["info:url"]).url
                store_json["info:url"] = url
                hbase_client.insert_data("news_data", store_json)
                print store_json["info:url"], "finished"
            except Exception as e:
                print traceback.print_exc()
                error.write("/home/abc/wechart_data/1/{name}.txt".format(name=i)+'\n')
                print "url error"
    error.close()
    # res = requests.get("http://www.baidu.com/link?url=y8p0MMA-vVKgoYNLNw6YvSzvkSwvAmJ-UZYLbBmjW5ywb3aJmFmZZPyzqxdAgWs7q8iUR7LIBbyil113GRlSva")
    # print res.url