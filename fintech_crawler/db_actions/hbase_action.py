import sys
import hashlib
from hbase import Hbase
from hbase.ttypes import *
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from settings import HBASE_HOST, HBASE_PORT
reload(sys)
sys.setdefaultencoding('utf8')


class HBASEAction(object):

    def __init__(self):
        transport = TTransport.TBufferedTransport(TSocket.TSocket(HBASE_HOST, HBASE_PORT))
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = Hbase.Client(protocol)
        transport.open()

    def generate_md5(self, _str):
        return hashlib.md5(_str.encode('utf-8')).hexdigest()

    def create_table(self, table_name, *col_name):
        self.client.createTable(table_name, map(lambda column: ColumnDescriptor(column), col_name))

    def scan_table(self, table_name, columns, need_row=False):
        scanner = self.client.scannerOpen(table_name, "", columns, {})
        while True:
            r = self.client.scannerGet(scanner)
            if not r:
                break
            if need_row:
                yield dict(dict(map(lambda (k, v): (k, v.value.encode("utf-8")), r[0].columns.items())), **{"row": r[0].row})
            else:
                yield dict(map(lambda (k, v): (k, v.value.encode("utf-8")), r[0].columns.items()))

    def insert_data(self, table_name, columns):
        raw_key = self.generate_md5(columns["info:url"])
        self.client.mutateRow(bytes(table_name), bytes(raw_key),
                              map(lambda (k, v): Mutation(column=bytes(k), value=bytes(v)), columns.items()), {})
        return True

    def url_exists(self, table_name, row_key):
        return self.client.getRow(bytes(table_name), bytes(row_key), {})

    def get_raw(self, table_name, url, column):
        row_key = self.generate_md5(url)
        data = self.client.getRow(bytes(table_name), bytes(row_key), {})
        if data:
            return data[0].columns.get(column).value.decode("utf-8")
        return data


if __name__ == "__main__":
    temp = HBASEAction()
    print temp.get_raw("url_schedule", "http://stock.cnstock.com/stock/smk_jjdx/201703/4042625.htm", "info:url")
    # print temp.insert_data("news_data", {"info:url": "www.baidu.com"})
    # num = 1
    # line = temp.scan_table("news_data", ["info:url", "info:content", "info:title", "info:source", "info:laiyuan",
    #                                      "info:author",
    #                                      "info:publish_time"])
    # while num:
    #     data = line.next()
    #     for k in data:
    #         print k, ":", data[k]
    #     num -= 1
    #     line.next
    pass

