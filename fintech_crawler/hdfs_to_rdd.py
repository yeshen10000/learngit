# coding=utf-8
import json
from news_feed.cn_stock import CNStock
from news_feed.cs_stock import CSStock
from news_feed.stcn_stock import STCNStock
from news_feed.cc_stock import CCStock
from news_feed.chinaipo_stock import ChinaIpoStock
from news_feed.jingji21_stock import JingJi21Stock
from news_feed.p5w_stock import P5WStock
from news_feed.wabei_stock import WaBeiStock
from pyspark import *
from pyspark.streaming import StreamingContext, StreamingListener

# 解析函数
route = {
    "CNStock": CNStock,
    "STCNStock": STCNStock,
    "CSStock": CSStock,
    "CCStock": CCStock,
    "ChinaIpoStock": ChinaIpoStock,
    "JingJi21Stock": JingJi21Stock,
    "P5WStock": P5WStock,
    "WaBeiStock": WaBeiStock
}


def field_detection(data):
    check_fields = ["info:parse_func", "info:url"]
    for field in check_fields:
        if field not in data:
            return False
    return True


def main():
    # 生成sc和SparkStreamingContext
    check_point_path = "hdfs://abc-cloudera004:8020/abc_crawler_data/sparkstreaming_checkpoint/"

    def func_to_create_scc():
        sc = SparkContext(appName="HDFS streaming")
        ssc = StreamingContext(sc, 8)
        ssc.checkpoint(check_point_path)
        sparkstreaming = ssc.textFileStream("hdfs://abc-cloudera004:8020/abc_crawler_data/page_index/").checkpoint(8)
        data = sparkstreaming.map(lambda line: json.loads(line))
        ne = data.filter(lambda d: field_detection(d))\
                 .filter(lambda d: d["info:parse_func"] in route) \
                 .filter(lambda d: not route[d["info:parse_func"]]().is_detect_anti(html=d["html"], params=d)) \
                 .map(lambda d: route[d["info:parse_func"]]().parse_content(d["html"], d))
        ne.pprint(30)
        return ssc

    # 监听hdfs指定目录
    check_ssc = StreamingContext.getOrCreate(check_point_path, func_to_create_scc)
    check_ssc.start()
    check_ssc.awaitTermination()


if __name__ == "__main__":
    """
    集群运行命令 nohup /usr/local/spark2/bin/spark-submit --py-files /home/szliu/fintech_crawler/spark_submit_library/db_actions.zip,/home/szliu/fintech_crawler/spark_submit_library/hbase.zip --conf spark.pyspark.virtualenv.enabled=true --conf spark.pyspark.virtualenv.type=native --conf spark.pyspark.virtualenv.requirements=/home/szliu/venv/crawler/requirements.txt --conf spark.pyspark.virtualenv.bin.path=/usr/local/python2.7/bin/virtualenv --conf spark.pyspark.python=/home/szliu/venv/crawler/bin/python2.7 /home/szliu/fintech_crawler/hdfs_to_rdd.py --executor-memory 2G --total-executor-cores 2 >> /niub/szliu/sparkstreaming.log 2>&1 &
    """
    main()
