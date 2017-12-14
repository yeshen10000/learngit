# encoding: utf-8
import sys
import json
sys.path.append("..")
import traceback
from pyquery import PyQuery
from db_actions.hbase_action import HBASEAction
from db_actions.redis_action import RedisAction


hbase_action = HBASEAction()
redis_action = RedisAction()


def upload_hbase(func):

    def wrap(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            hbase_action.insert_data("news_data", data)
            return "data save in hbase"
        except Exception as e:
            traceback.print_exc()
            print kwargs["params"]["info:url"], "css selector error"
            return kwargs["params"]["info:url"], "css selector error"

    return wrap


def html_to_dom(is_detect_anti):

    def wrap(*args, **kwargs):
        try:
            if not kwargs["html"]:
                return True

            dom = PyQuery(kwargs["html"])
            _params = {k: v for k, v in kwargs["params"].items() if k.startswith("info")}
            if is_detect_anti(*args, dom=dom):
                redis_action.priority_queue_push("anti_crawler_url_queue", [
                    json.dumps(_params), _params["info:priority"]
                ])
                return True
            return False
        except Exception as e:
            traceback.print_exc()
            return True
    return wrap

