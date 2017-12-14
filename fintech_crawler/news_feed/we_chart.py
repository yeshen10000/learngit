# encoding: utf-8
from datetime import datetime
from base_stock import BaseStock
from supervisor import upload_hbase, html_to_dom


class WeChart(BaseStock):

    allow_domains = ["wechart.cn"]

    def is_detail_url(self, dom):
        return dom("div.page-content")

    @upload_hbase
    def parse_detail_url(self, dom, params):
        """
        获取所有url, 放入hbase队列, 并解析数据
        :param dom:
        :param url:
        :return:
        """
        store_json = {
            "info:title": dom("div#img-content > h2#activity-name").text(),
            "info:publish_time": dom("div.rich_media_meta_list > em#post-date").text(),
            "info:source": dom("a#post-user").text(),
            "info:author": dom("div.rich_media_meta_list > em").eq(1).text(),
            "info:content": self.link_analysis.strip_html5_whitespace(dom("div#page-content").html()),
            "info:tag": dom("div.model-tags > a").text(),
            "info:dese": "",
            "info:crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "info:url": "",
            "info:channel": "wecharts",
            "info:laiyuan": "http://weixin.sogou.com/weixin",
            "info:contain_image": "True" if dom("div#page-content")("img") else "False"
        }
        return store_json

    @html_to_dom
    def is_detect_anti(self, dom):
        return False


if __name__ == "__main__":
    temp = WeChart()

