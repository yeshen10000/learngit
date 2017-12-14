# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class CCStock(BaseStock):

    allow_domains = ["ccstock.cn"]

    def is_detail_url(self, dom):
        return dom("div#newscontent")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        info = dom("div.sub_bt > span").text()
        info_list = info.split("  ")
        source, publish = "", ""
        for line in info_list:
            if line.find(u"文章来源") > -1:
                source = line.split("：")[-1]
            elif line.find(u"更新时间") > -1:
                publish = line.split("：")[-1]

        store_json = {
            "info:title": dom("div.bt > h1").text(),
            "info:publish_time": publish,
            "info:source": source,
            "info:author": "",
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div#newscontent").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div#left > a").text(),
            "info:laiyuan": dom("div.logo > a").attr("href"),
            "info:contain_image": "True" if dom("div#newscontent")("img") else "False"
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
    temp = CCStock()

