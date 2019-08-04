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

import pandas as pd
import xlrd

# 转换某一列为字符串
# df = pd.DataFrame(pd.read_excel('train_data.xlsx', converters={'visitor_id': str}))
# 转换所有列为字符串
df = pd.DataFrame(pd.read_excel('test_data/test_excel.xlsx', dtype=str))

# 数据预处理
# 1. 填补 visitor_id 为空的缺省值（非空字符串），以特定值填充某一列的空值
df["visitor_id"] = df["visitor_id"].fillna(0)

# 2. 删除某列包含特殊值的行
df = df[~ df['证券名称'].str.contains('联通')]



# 常用操作
# 1. 删除行（根据行索引）
df = df.drop("row_id")
# 删除行（根据行号）
df = df.drop(df.index[6])
# 删除特定数值的行
df = df[df['成交金额'] > 10000]
# 删除某列包含特殊字符的行
df = df[~ df['证券名称'].str.contains('联通')]


# 2. 删除列
df = df.drop(['id'], axis=1)
# 删除多列（列集合）
df = df.drop(columns=['B', 'C'])




# # 数据统计
# # 读取前五条数据
# df.head()
# # 读取某列
# created_time = df['created_time']
# for one_time in created_time:
#     date = one_time.split(" ")[0]
#     time = one_time.split(" ")[1]
#     print(date, time)
