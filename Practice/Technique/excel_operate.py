"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/8/3 12:07
 @File    : excel_operate.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import numpy
import pandas as pd
import matplotlib
import pyecharts


# 转换某一列为字符串
# df = pd.DataFrame(pd.read_excel('train_data.xlsx', converters={'visitor_id': str}))
# 转换所有列
df = pd.DataFrame(pd.read_excel('train_data.xlsx', dtype=str))

# 数据预处理
# 1. 填补 visitor_id 为空的缺省值，以特定值填充某一列的空值
df["visitor_id"] = df["visitor_id"].fillna(0)
print(df["visitor_id"][:30])

# # 数据统计
# # 读取前五条数据
# works.head()
# # 读取某列
# created_time = works['created_time']
# for one_time in created_time[:10]:
#     date = one_time.split(" ")[0]
#     time = one_time.split(" ")[1]
#     print(date, time)
