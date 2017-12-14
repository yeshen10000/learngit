import requests
import json
import sys
import json
sys.path.append("..")
import traceback
from random import choice
from db_actions.redis_action import RedisAction


class ProxyCheck(object):

    check_urls = ["http://news.cnstock.com/news/sns_yw/index.html"]

    def __init__(self):
        self.redis_action = RedisAction()

    def check_rules(self, proxy_url):
        for curl in self.check_urls:
            try:
                proxy_res = requests.get(curl, proxies={"http": proxy_url}, timeout=20)
                if proxy_res.status_code not in [200]:
                    return False
            except Exception as e:
                traceback.print_exc()
                return False
        else:
            return True

    def period_check(self):
        for proxy_url in self.redis_action.members_set("proxy_set"):
            if not self.check_rules(proxy_url):
                self.redis_action.pop_set("proxy_set", proxy_url)
                print "proxy {} is disabled".format(proxy_url)
            else:
                print "proxy {} is enabled".format(proxy_url)

    def add_new(self):
        url_list = [
            "http://dec.ip3366.net/api/?key=20171207221341061&getnum=30&anonymoustype=3&filter=1&area=1&sarea=1&formats=2&proxytype=0",
            "http://dec.ip3366.net/api/?key=20171207221341061&getnum=30&anonymoustype=4&filter=1&area=1&sarea=1&formats=2&proxytype=0"
        ]
        res = requests.get(choice(url_list))
        proxy_json = json.loads(res.text)
        for proxy in proxy_json:
            proxy_url = "http://{}:{}".format(proxy["Ip"], proxy["Port"])
            for curl in self.check_urls:
                try:
                    proxy_res = requests.get(curl, proxies={"http": proxy_url}, timeout=10)
                    if proxy_res.status_code not in [200]:
                        print "proxy {} is disabled".format(proxy_url)
                        break
                except Exception as e:
                    traceback.print_exc()
                    print "proxy {} is disabled".format(proxy_url)
                    break
            else:
                self.redis_action.add_set("proxy_set", proxy_url)
                print "proxy {} is enabled".format(proxy_url)


if __name__ == "__main__":
    temp = ProxyCheck()
    command = sys.argv[1]
    route = {"add_new": temp.add_new,
             "period_check": temp.period_check}
    route[command]()





