# encoding: utf-8
import json
from datetime import datetime
from datetime import timedelta
import sys
sys.path.append("..")
from db_actions.hbase_action import HBASEAction
from db_actions.redis_action import RedisAction


class CrawlProducer(object):

    """
    定时扫描 hbase表中应该爬去的url, 然后写入crawl_task_queue
    crontab -e
    * * * * * python /home/szliu/fintech_crawler/period/crawl_task_producer.py >> /niub/crontab_log/crontab.log 2>&1
    hbase info
        url： 网址
        next_time： 下一次抓取时间
        last_time： 最近一次抓取时间
        channel： url所属频道
        priority： 优先级
        parse_func： url的解析函数
        once_every_minutes： 多少分钟抓一次
    """
    def __init__(self):
        self.redis_action = RedisAction()
        self.hbase_action = HBASEAction()

    def run(self, queue_name, hbase_table_name):
        # 扫描表
        count = 0
        for hbase_dict in self.hbase_action.scan_table(hbase_table_name, ["info:url",
                                                                          "info:priority",
                                                                          "info:parse_func",
                                                                          "info:next_time",
                                                                          "info:once_every_minutes"]):
            base_time = datetime.now()
            rate = int(hbase_dict["info:once_every_minutes"])
            # 判断是否到达爬取时间
            if hbase_dict["info:next_time"] <= base_time.strftime("%Y-%m-%d %H:%M:%S"):
                crawl_dict = {
                    "info:url": hbase_dict["info:url"],
                    "info:priority": hbase_dict["info:priority"],
                    "info:parse_func": hbase_dict["info:parse_func"],
                }
                count += 1
                self.redis_action.priority_queue_push(queue_name, json.dumps(crawl_dict),
                                                      int(crawl_dict["info:priority"]))
                # 修改表中下一次的时间
                self.hbase_action.insert_data(hbase_table_name, {"info:last_time": base_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                 "info:url": hbase_dict["info:url"],
                                                                 "info:next_time": (base_time + timedelta(minutes=rate)).strftime("%Y-%m-%d %H:%M:%S")})
        print "[%s] write %s finished" % (datetime.now(), count)


if __name__ == "__main__":
    temp = CrawlProducer()
    temp.run("crawl_task_queue", "hub_page")

