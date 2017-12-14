# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class JingJi21Stock(BaseStock):

    allow_domains = ["21jingji.com"]

    def is_detail_url(self, dom):
        return dom("div.txtContent")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        store_json = {
            "info:title": dom("div.titleHead > h1").text(),
            "info:publish_time": dom("div.titleHead > div.newsDate").text(),
            "info:source": dom("div.titleHead > div.newsInfo").eq(0).text(),
            "info:author": dom("div.titleHead > div.newsInfo > a").text(),
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div.txtContent").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": "",
            "info:laiyuan": dom("div.headLogo > a").attr("href"),
            "info:contain_image": "True" if dom("div.txtContent")("img") else "False"
        }
        return store_json

    @html_to_dom
    def is_detect_anti(self, dom):
        return False

    def link_filter(self, url=""):
        if url.endswith("html"):
            return False
        if url.endswith("htm"):
            return False
        return False


if __name__ == "__main__":
    temp = JingJi21Stock()

