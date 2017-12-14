# encoding: utf-8
import json
import sys
sys.path.append("..")
from pyquery import PyQuery
from supervisor import upload_hbase, html_to_dom
from db_actions.redis_action import RedisAction
from utilty.link_analysis import LinkExtractor


class BaseStock(object):

    def __init__(self):
        self.link_analysis = LinkExtractor()
        self.redis_action = RedisAction()

    def is_detail_url(self, dom):
        """
        判断url是否详情页
        :param dom:
        :return True or False:
        """
        return True

    def get_channel(self, dom):
        return ""

    def parse_content(self, response_text, params):
        """
        判断是否时详情页, 如果是则解析网页内容, 如果不是则提取网页所有网址
        :param response_text: 网页内容
        :param params: {'info:url': 'info:priority': 'info:pase_func': ,}
        :return:
        """
        _params = {k: v for k, v in params.items() if k.startswith("info")}
        dom = PyQuery(response_text.strip())
        if self.is_detail_url(dom):
            return self.parse_detail_url(dom=dom, params=_params)
        else:
            return self.parse_other_url(dom=dom, params=_params)

    def parse_other_url(self, dom, params):
        """
        获取所有url, 并写入depfilter_task_queue
        :param dom:
        :param params:
        :return:
        """
        result_list = []
        channel = self.get_channel(dom)
        for e in dom.find('a'):
            sub_url = PyQuery(e).attr('href')
            if sub_url and sub_url.startswith("."):
                sub_url = self.link_analysis.url_join(params["info:url"], sub_url)

            if self.link_analysis.url_legal(sub_url, self.allow_domains):
                if not self.link_filter(sub_url):
                    # 存入redis队列
                    _params = dict(params.copy(), **{"info:url": sub_url, "info:channel": channel})
                    result_list.extend([json.dumps(_params), int(_params["info:priority"])])
        self.redis_action.priority_queue_push("dupfilter_task_queue", *result_list)
        return "parse urls"

    @upload_hbase
    def parse_detail_url(self, dom, params):
        pass

    @html_to_dom
    def detect_anti(self, ):
        pass

    def link_filter(self, url):
        return False


if __name__ == "__main__":
    temp = BaseStock()
    print temp
    # print temp.parse_content("aaaaa")

