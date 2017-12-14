# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class P5WStock(BaseStock):

    allow_domains = ["p5w.net"]

    def is_detail_url(self, dom):
        return dom("div.article_content2")

    @upload_hbase
    def parse_detail_url(self, dom, url):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        store_json = {
            "info:title": dom("div.newscontent_right2 > h1").text(),
            "info:publish_time": dom("div.content_info > span.left > time").text(),
            "info:source": "",
            "info:author": dom("div.zhuoze > a").text(),
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div.article_content2").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div.content_info > span.left > span").eq(0).text(),
            "info:laiyuan": dom("div.logo-wrap > a.logo").attr("href"),
            "info:contain_image": "True" if dom("div.article_content2")("img") else "False"
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
    temp = P5WStock()

