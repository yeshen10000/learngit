# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom

class WaBeiStock(BaseStock):

    allow_domains = ["wabei.cn"]

    def is_detail_url(self, dom):
        return dom("div.subject-content")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        store_json = {
            "info:title": dom("div.subject > h1").text(),
            "info:publish_time": dom("div.attr > span.time").text(),
            "info:source": dom("div.attr > span.source").text(),
            "info:author": dom("div.attr > span.author").text(),
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div.subject-content").html()),
            "info:tag": dom("div.model-tags > a").text(),
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div.breadcrumb > a").text(),
            "info:laiyuan": dom("div#nav > a.brand").attr("href"),
            "info:contain_image": "True" if dom("div.subject-content")("img") else "False"
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
        return True


if __name__ == "__main__":
    temp = WaBeiStock()

