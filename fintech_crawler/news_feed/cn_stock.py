# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class CNStock(BaseStock):

    allow_domains = ["cnstock.com"]

    def is_detail_url(self, dom):
        return dom("div#qmt_content_div")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        store_json = {
            "info:title": dom("h1").text(),
            "info:publish_time": dom("div.bullet > span.timer").text() or dom("div.sub-title > span.time").text(),
            "info:source": dom("div.bullet > span.source").text() or dom("div.sub-title").contents()[-1].strip(),
            "info:author": dom("div.bullet > span.author").text(),
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div#qmt_content_div").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div.breadcrumbs > div.container a").text() or dom("ul.breadcrumbs > li > a").text(),
            "info:laiyuan": dom("div.logo > a").attr("href"),
            "info:contain_image": "True" if dom("div#qmt_content_div")("img") else "False"
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
        if url.startswith("http://irm.cnstock.com/content_company"):
            return False
        return True


if __name__ == "__main__":
    temp = CNStock()
    print temp.is_detect_anti(html="<a>aaa</a>", param={})

