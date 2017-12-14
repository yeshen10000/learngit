# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class CSStock(BaseStock):

    allow_domains = ["cs.com.cn"]

    def is_detail_url(self, dom):
        return dom("div.artical_c")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param params:
        :return:
        """
        store_json = {
            "info:title": dom("div.artical_t > h1").text(),
            "info:publish_time": dom("div.artical_t > span.Ff").text(),
            "info:source": dom("div.artical_t > span").eq(0).text(),
            "info:author": dom("div.artical_t > span").eq(1).text(),
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div.artical_c").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div.secbar > a").text(),
            "info:laiyuan": dom("div.nav_line2 > a.logo_cs").attr("href"),
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
        return True


if __name__ == "__main__":
    temp = CSStock()
    print temp.allow_domains
    t = CSStock.is_detail_url.__func__()


