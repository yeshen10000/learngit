# encoding: utf-8
import time
import json
from pyspark import *
from datetime import datetime

# project_path = "/home/abc/PycharmProjects/spider/spark_submit_library"


def dupfilter_task_work(data, hb_action, redis_action, crawl_name, table_name):
    """
    取出待处理的url, 查询hbase表是否存在, 不存在放入crawl_task_queue
    :param data:
    :param hb_action:
    :param redis_action:
    :param crawl_name:
    :param table_name:
    :return:
    hbase "url_schedule" info
        url
        first_time
        last_time
        channel
        status
        is_hub
    """
    raw_key = hb_action.generate_md5(data["info:url"])
    crawl_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 判断该url是否在hbase中
    if not hb_action.url_exists(table_name, raw_key):
        # 向hbase里面写信息
        columns = {
            "info:first_time": crawl_time,
            "info:last_time": crawl_time,
            "info:status": "pending",
            "info:is_hub": ""
        }
        hb_action.insert_data(table_name, dict(columns, **data))
        data.pop("info:channel")
        redis_action.priority_queue_push(crawl_name, json.dumps(data), int(data["info:priority"]))
        return "create"
    else:
        # 更新对应数据
        hb_action.insert_data(table_name, {"info:last_time": crawl_time,
                                           "info:status": "pending",
                                           "info:channel": "",
                                           "info:url": data["info:url"]})
        if hb_action.get_raw(table_name, data["info:url"], "info:is_hub"):
            redis_action.priority_queue_push(crawl_name, json.dumps(data), int(data["info:priority"]))
        return "update"


if __name__ == "__main__":
    """
    运行参数
    nohup /usr/local/spark2/bin/spark-submit --master spark://abc-cloudera001:7077 --py-files /home/szliu/fintech_crawler/spark_submit_library/db_actions.zip,/home/szliu/fintech_crawler/spark_submit_library/hbase.zip --conf spark.pyspark.virtualenv.enabled=true --conf spark.pyspark.virtualenv.type=native --conf spark.pyspark.virtualenv.requirements=/home/szliu/venv/crawler/requirements.txt --conf spark.pyspark.virtualenv.bin.path=/usr/local/python2.7/bin/virtualenv dupfilter_task_worker.py --executor-memory 2G --total-executor-cores 2 >> /niub/szliu/dupfilter_task_worker.log 2>&1 &
    nohup /usr/local/spark2/bin/spark-submit --py-files /home/szliu/fintech_crawler/spark_submit_library/db_actions.zip,/home/szliu/fintech_crawler/spark_submit_library/hbase.zip --conf spark.pyspark.virtualenv.enabled=true --conf spark.pyspark.virtualenv.type=native --conf spark.pyspark.virtualenv.requirements=/home/szliu/venv/crawler/requirements.txt --conf spark.pyspark.virtualenv.bin.path=/usr/local/python2.7/bin/virtualenv dupfilter_task_worker.py --executor-memory 2G --total-executor-cores 2  >> /niub/szliu/dupfilter_task_worker.log 2>&1 &
    """
    sc = SparkContext(appName="dupfilter_task_work")
    # sc.addPyFile("{base_path}/redis.zip".format(base_path=project_path))
    # sc.addPyFile("{base_path}/pyhdfs.zip".format(base_path=project_path))
    from db_actions.hbase_action import HBASEAction
    from db_actions.redis_action import RedisAction
    redis_action = RedisAction()
    while True:
        data_lines = redis_action.priority_queue_pop("dupfilter_task_queue", 50)
        if any(data_lines):
            news = sc.parallelize(data_lines).filter(lambda x: x).map(lambda x: dupfilter_task_work(x, HBASEAction(),
                                                                      RedisAction(), "crawl_task_queue", "url_schedule"))
            # news.count()
            print news.collect()
        else:
            time.sleep(10)

