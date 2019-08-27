"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 
 --------------------------------
 @Time    : 2019/8/27 20:20
 @File    : pandas_Operation.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import pandas as pd
import numpy as np
from copy import deepcopy

## 1. read_cvs
# 当读取的数据量很大时，请尝试添加这个参数：nrows
pd.read_csv(nrows=5)
# dtype 声明列的类型
df = pd.DataFrame(dtype={'col1': str, 'c2': int})


## 2. select_dtypes 在读取表之后，每个列的默认数据类型可以是bool、int64、float64、object、category、timedelta64或datetime64。
df.select_dtypes(include=['float64', 'int64'])


## 3. copy 复制 df
df1 = pd.DataFrame({'a': [0, 0, 0], 'b': [1, 1, 1]})
df2 = df1
df2['a'] = df2['a'] + 1
df1.head()

# df2 = df1不是复制df1并将其赋值给df2，而是设置一个指向df1的指针。所以df2的任何变化都会导致df1的变化
df2 = df1.copy()
# 或者
df3 = deepcopy(df1)


## 4. map
# 数据转换。keys 是旧值，values 是新值
level_map = {1: 'high', 2: 'medium', 3: 'low'}
df['c_level'] = df['c'].map(level_map)


## 5. apply
# 创建一个新列，其中包含其他列内容作为输入
# 缺点：速度慢
def rule(x, y):
    if x == 'high' and y > 10:
        return 1
    else:
        return 0

df = pd.DataFrame({'c1': ['high', 'high', 'low', 'low'], 'c2': [0, 23, 17, 4]})
df['new'] = df.apply(lambda x: rule(x['c1'], x['c2']), axis=1)
df.show()


## 6. value_counts 查看值分布
df['col1'].value_counts()
# normalize = True：如果你想查看频率而不是计数。
# dropna = False：如果你还想在统计中包含缺失值。
# sort = False：按值而不是按计数排序的统计结果。
# df['c'].value_counts().reset_index()：如果你想将stats表转换为pandas dataframe并对其进行操作。


## 7. 缺失值数量
# .isnull() 和 .sum() 来计算指定列中缺失值的数量。
df = pd.DataFrame({'id': [1, 2, 3], 'c1': [0, 0, np.nan], 'c2': [np.nan, 1, 1]})
df = df[['id', 'c1', 'c2']]
df['num_nulls'] = df[['c1', 'c2']].isnull().sum(axis=1)
df.head()


## 8. 选择特定多个 ID 的行
df_filter = df['ID'].isin(['A001', 'C022'])
print(df[df_filter])


## 9. 百分位组  将一列的值分类为几组。
# 比如前5%的值分为组1，5-20%的值分为组2，20-50%的值分为组3，底部50%的值分为组4
cut_points = [np.percentile(df['col'], i) for i in [50, 80, 95]]
df['group'] = 1
for i in range(3):
    df['group'] = df['group'] + (df['col'] < cut_points[i])


## 10. to_csv
# 准确地打印出写入文件的前五行
print(df[:5].to_csv())

# 处理混合在一起的整数和缺失值。
# 如果一个列同时包含缺失值和整数，那么数据类型仍然是float而不是int。
# 导出表时，可以添加 float_format='%.0f' ，将所有浮点数化为整数。
# 如果你只想要所有列的整数输出，请使用此技巧。
