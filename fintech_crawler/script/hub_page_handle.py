# encoding: utf-8
import csv
import sys
sys.path.append("..")
from datetime import datetime
from datetime import timedelta
from db_actions.hbase_action import HBASEAction


class HubPage(object):

    def __init__(self):
        self.hbase_action = HBASEAction()

    def put(self, *args, **kwargs):
        self.hbase_action.insert_data(*args, **kwargs)

    def scan(self, table_name, columns, need_row=False):
        return self.hbase_action.scan_table(table_name, columns, need_row)


if __name__ == "__main__":

    csvFile = open("hub_page.csv", "r")
    news_list = csv.reader(csvFile)  # 返回的是迭代类型

    # news_list = [
    #     ("http://news.cnstock.com/industry/sid_rdjj", 99, 5, "CNStock"),
    #     ("http://news.cnstock.com/industry/sid_zxk", 99, 5, "CNStock")
    # ]
    temp = HubPage()
    for index, (url, priority, rate, analysis) in enumerate(news_list):
        print url, priority, rate, analysis
        last_time = datetime.now()
        temp.put("hub_page", columns={"info:url": url, "info:last_time": last_time.strftime("%Y-%m-%d %H:%M:%S"),
                                      "info:next_time": (last_time + timedelta(minutes=int(rate))).strftime("%Y-%m-%d %H:%M:%S"),
                                      "info:priority": str(priority),
                                      "info:once_every_minutes": str(rate),
                                      "info:parse_func": analysis})

    for line in temp.scan("hub_page", ["info:url"]):
         print line
