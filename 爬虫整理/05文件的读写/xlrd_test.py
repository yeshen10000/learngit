# encoding: utf-8

import requests
from bs4 import BeautifulSoup
import os
import xlrd


data = xlrd.open_workbook('data.xlsx')


#指的是通过顺序索引获取第一个工作表
sheet = data.sheets()[0]
# sheet = data.sheet_by_index(0)#指的是通过顺序索引获取第一个工作表
# sheet = data.sheet_by_name(u'Sheet1')#指的是通过名称获取工作表

nrows = sheet.nrows#获取工作表的总行数
ncols = sheet.ncols#获取工作表的总列数

#指的是获取某个行的整个信息
print(sheet.row_values(100))

#指的是获取某个列的整个信息
print(sheet.col_values(3))
#指的是获取某个单元格的信息
print(sheet.cell(0,0).value)

for i in range(1,16):
    print(sheet.cell(i,1).value)