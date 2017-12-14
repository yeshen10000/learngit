# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class ChinaIpoStock(BaseStock):

    allow_domains = ["chinaipo.com"]

    def is_detail_url(self, dom):
        return dom("div.newscont")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        info = dom("p.news-from").text()
        info_list = info.split("·")
        info_dict = {k: v.strip() for k, v in zip(["source", "publish_time", "author"], info_list[:-1])}

        store_json = {
            "info:title": dom("div.crumb > h1.tt-news").text(),
            "info:author": "",
            "info:publish_time": "",
            "info:source": "",
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div.newscont").html()),
            "info:tag": dom("div.keywdbox > a").text(),
            "info:dese": dom("div.artical-summary").text(),
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div.crumb-title > a").text(),
            "info:laiyuan": dom("div#nav > a.brand").attr("href"),
            "info:contain_image": "True" if dom("div.crumb")("img") else "False"
        }
        return dict(store_json, **info_dict)

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
    temp = ChinaIpoStock()

