#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-11-15 14:33:21
# Project: cnstock
import sys
sys.path.append("/home/szliu/fintech_crawler/")
reload(sys)
sys.setdefaultencoding('utf8')
import json
from random import choice
from datetime import datetime
from pyspider.libs.base_handler import *
from db_actions.hdfs_action import FileStore
from db_actions.redis_action import RedisAction


class Handler(BaseHandler):
    file_store = FileStore()
    redis_action = RedisAction()

    crawl_config = {
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    }

    @every(minutes=1)
    def on_start(self):
        data_list = self.redis_action.priority_queue_pop("crawl_task_queue", 0)
        proxy_list = self.redis_action.get_random_set("crawler_set", 3)

        for data in data_list:
            if proxy_list:
                choice_proxy = choice(proxy_list)
                self.crawl(data["info:url"], callback=self.index_page, save=data,
                           proxy="{}:{}".format(choice_proxy["Ip"], choice_proxy["Port"]), headers=self.headers)
            else:
                self.crawl(data["info:url"], callback=self.index_page, save=data, headers=self.headers)

    @catch_status_code_error
    def index_page(self, response):
        if response.status_code in [404, 403, 302, 312, 500]:
            return {'result': response.url,
                    'html': response.save["html"],
                    'status_code': response.status_code,
                    'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if isinstance(response.text, unicode):
            response.save.update({"html": response.text})
        else:
            response.save.update({"html": response.text.decode(response.encoding)})
        self.file_store.save(json.dumps(response.save))
        return {'result': response.url,
                'html': response.save["html"],
                'crawl_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
