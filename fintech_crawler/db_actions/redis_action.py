# encoding: utf-8
import sys
import redis
import json
from settings import REDIS_HOST, REDIS_PORT
reload(sys)
sys.setdefaultencoding('utf8')


class RedisAction(object):

    """
    redis的操作
    任务队列crawl_task_queue用于存放等待爬取的url的链接
    如果需要修改hbase状态,则需要传入hbase的操作对象
        RedisAction(HbaseAction()),默认不需要修改无需传入
    任务队列dupfilter_task_queue用于存放等待去重的url的链接
    """

    def __init__(self, hbase_action=""):
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        self.hbase_action = hbase_action

    def add_set(self, queue_name, *args):
        self.redis.sadd(queue_name, *args)

    def get_random_set(self, queue_name, number):
        return self.redis.srandmember(queue_name, number=number)

    def pop_set(self, queue_name, *args):
        return self.redis.srem(queue_name, *args)

    def members_set(self, queue_name):
        for member in self.redis.smembers(queue_name):
            yield member

    def priority_queue_pop(self, queue_name, num, table_name="", status_change=False):
        """
        优先级队列pop出第一个元素
        :param queue_name: 优先级队列名字
        :param num: pop的数量,
        :param table_name: url进度表名字,不修改状态就不用提供
        :param status_change: 是否更改hbase的状态, 一般不需要修改
        :return: (value, scores) or []
        """
        pipe = self.redis.pipeline()
        pipe.zrange(queue_name, 0, num, withscores=True)
        pipe.zremrangebyrank(queue_name, 0, num)
        pipe_list = pipe.execute()[0]
        if not pipe_list:
            return []
        result_list = []
        for data in pipe_list:
            # print data
            data = json.loads(data[0])
            if status_change:
                self.hbase_action.insert_data(table_name, {"info:url": data["info:url"], "info:status": "finished"})
            result_list.append(data)
        return result_list

    def priority_queue_push(self, queue_name, *args, **kwargs):
        """
        优先级队列插入元素
        :param queue_name: 优先级队列名字
        :param value: 插入值
        :param priority: 优先级(整型)
        :return: None
        """
        if any(args):
            self.redis.zadd(queue_name, *args, **kwargs)


if __name__ == "__main__":
    # temp = RedisAction()
    temp = RedisAction()
    # print temp.priority_queue_pop("proxy_queue", 0)
    pass
