# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class STCNStock(BaseStock):

    allow_domains = ["stcn.com"]

    def is_detail_url(self, dom):
        return dom("div.txt_con")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        info = dom("div.intal_tit > div.info").text()
        publish, source = info.split(u"来源：") if len(info.split(u"来源：")) >= 2 else (info.split(u"来源：")[0], " ")
        sotre_json = {
            "info:title": dom("div.intal_tit > h2").text(),
            "info:publish_time": publish.strip(),
            "info:source": source.strip(),
            "info:author": "",
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div.txt_con").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": dom("div.website > a").text(),
            "info:laiyuan": dom("div.menu_con > ul.mainNav > li").eq(0)("a").attr("href"),
            "info:contain_image": "True" if dom("div#qmt_content_div")("img") else "False"
        }
        return sotre_json

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
    temp = STCNStock()

