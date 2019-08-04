"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description :
 --------------------------------
 @Time    : 2019/8/4 17:04
 @File    : test.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import DataFrame, Series
# from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression

# 读取文件
datafile = 'test_excel.xlsx'  # 文件所在位置，u为防止路径中有中文名称，此处没有，可以省略
data = pd.read_excel(datafile)  # datafile是excel文件，所以用read_excel,如果是csv文件则用read_csv
examDf = DataFrame(data)

# 数据清洗,比如第一列有可能是日期，这样的话我们就只需要从第二列开始的数据，
# 这个情况下，把下面中括号中的0改为1就好，要哪些列取哪些列
new_examDf = examDf.ix[:, 1:]

# 检验数据
print(new_examDf.describe())  # 数据描述，会显示最值，平均数等信息，可以简单判断数据中是否有异常值
print(new_examDf[new_examDf.isnull() == True].count())  # 检验缺失值，若输出为0，说明该列没有缺失值

# 输出相关系数，判断是否值得做线性回归模型
print(new_examDf.corr())  # 0-0.3弱相关；0.3-0.6中相关；0.6-1强相关；

# 通过seaborn添加一条最佳拟合直线和95%的置信带，直观判断相关关系
# sns.pairplot(data, x_vars=['visitor_id'], y_vars='created_time', height=7, aspect=0.8, kind='reg')
