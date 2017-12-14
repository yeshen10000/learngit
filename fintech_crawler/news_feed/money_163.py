# encoding: utf-8
from pyquery import PyQuery
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class FinaceSina(BaseStock):

    allow_domains = ["money.163.com"]
    home_page = "http://money.163.com"

    def is_detail_url(self, dom):
        return dom("div#endText")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param params:
        :return:
        """
        title = dom("h1#artibodyTitle").text()
        artinfo1 = dom("div.artInfo")
        publish_time, source, channel = "", "", ""
        if artinfo1:
            publish_time = artinfo1("span#pub_date").text()
            source = artinfo1("span#media_name").text()
            channel = dom("div.fl > p.fl > a").text()
        artinfo2 = dom("div.page-info")
        if artinfo2:
            publish_time = artinfo2("span.time-source").text()
            source = artinfo2("span > a").filter(lambda x, this: PyQuery(this).attr("rel")).text()
            channel = dom("div.bread > a").text()

        store_json = {
            "info:title": title,
            "info:publish_time": publish_time,
            "info:source": source,
            "info:author": "",
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div#artibody").html()),
            "info:tag": "",
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": params["info:url"],
            "info:channel": channel,
            "info:laiyuan": self.home_page,
            "info:contain_image": "True" if dom("div#artibody")("img") else "False"
        }
        return store_json

    @html_to_dom
    def is_detect_anti(self, dom):
        return False


if __name__ == "__main__":
    temp = CSStock()
    print temp.allow_domains
    t = CSStock.is_detail_url.__func__()


