# encoding: utf-8
import sys
import os
from datetime import datetime
import pyhdfs
from settings import HDFS_HOST, HDFS_PORT
reload(sys)
sys.setdefaultencoding('utf8')


class HDFSAction(object):
    """
    hdfs 操作api
    """

    def __init__(self):
        hosts = ",".join(["{}:{}".format(host, HDFS_PORT) for host in HDFS_HOST])
        self.client = pyhdfs.HdfsClient(hosts=hosts,user_name="szliu", max_tries=5, retry_delay=5)

    def list(self, *argv, **kwargs):
        """
        列出目录下的文件
        :param path: hdfs路径
        :param kwargs:
        :return: list 目录下的文件夹
        """
        return self.client.listdir(*argv, **kwargs)

    def makedirs(self, *argv, **kwargs):
        self.client.mkdirs(*argv, **kwargs)

    def exists(self, *args, **kwargs):
        return self.client.exists(*args, **kwargs)

    def write(self, *args, **kwargs):
        """
        追加写入文件, 如果文件不存在则写入失败
        :param path: hdfs路径
        :param kwargs:
        :return: None
        """
        self.client.append(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self.client.open(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        删除hdfs目录
        :param args: path：路径, recursive=True 递归删除子目录
        :param kwargs:
        :return: True or False
        """
        self.client.delete(*args, **kwargs)


class FileStore(object):

    def __init__(self):
        self.file_path = "/abc_crawler_data"
        self.hdfs_action = HDFSAction()

    def save(self, content):
        time_flag = datetime.now()
        filename = "{base}-{minute}".format(base=time_flag.strftime("%Y-%m-%d_%H"), minute="%02d" % (time_flag.minute/5*5))
        file_path = os.path.join(self.file_path, time_flag.strftime("%Y-%m-%d_%Hh"), filename+".json")
        if not self.hdfs_action.client.exists(file_path):
            self.hdfs_action.client.create(file_path, "")
        self.hdfs_action.write(file_path, data=content+'\n', overwrite=False)


if __name__ == "__main__":
    temp = HDFSAction()
    print temp.list('/')
    # print temp.read('/abc_crawler_data/1.txt').read()
    pass

