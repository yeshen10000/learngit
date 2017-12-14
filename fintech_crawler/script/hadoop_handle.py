# encoding: utf-8
import sys
sys.path.append("..")
from db_actions.hdfs_action import HDFSAction
client = HDFSAction()


if __name__ == "__main__":
    for line in client.list("/").readlines():
        print line,
    # print client.delete("/abc_data/2017-11-23-19h.json")
    pass
