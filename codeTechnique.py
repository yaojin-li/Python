"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : python 技巧
    单独调试某几行代码段：Execute line in console(快捷键：Alt+Shift+E)
 --------------------------------------
 @File        : codeTechnique.py
 @Time        : 2018/11/7 22:24
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""


# =====================字典======================
# 1. 快速构建字典
dict_zip = dict(zip('abcd', range(4)))

# 2. 更新字典——1
dict1 = {'a':'1'}
dict2 = {'b':'2', 'c':'3'}
dictRes = dict(dict2, **dict1)  # 多参数添加字典
print(dictRes)   # {'b': '2', 'c': '3', 'a': '1'}
# 3. 更新字典——2
dict2.update(dict1)
print(dict2) # {'b': '2', 'c': '3', 'a': '1'}

# 4. 字典循环
dict3 = {'1':'a','2':'b','13':'c'}
for key in dict3:
    print(key)
for key in dict3.keys():
    if key.startswith('1'):
        print(dict3[key])

# 5. 用字典进行统计-合并同类项
nums = ['1', '22', '233', '4', '55']
from collections import defaultdict
dict5 = defaultdict(list)
for num in nums:
    key = len(num)
    dict5[key].append(num)
print(dict5)    # defaultdict(<class 'list'>, {1: ['1', '4'], 2: ['22', '55'], 3: ['233']})


# =====================列表======================
# 1. 嵌套list转一个list
more2oneList = [1, [2, [3, 4]]]
resList = []
def fun(more2oneList):
    for i in more2oneList:
        if isinstance(i,list):
            fun(i)  # 递归
        else:
            resList.append(i)
fun(more2oneList)
print(resList)  # [1, 2, 3, 4]

# 2. 嵌套list转一个list
more2oneList_ = [[[1,2],[100,101],[3]],[[7,8]]]
print([z for x in more2oneList_ for y in x for z in y])  # [1, 2, 100, 101, 3, 7, 8]

# 3. 统计列表元素个数
nums = [1, 2, 3, 4, 4, 3, 2, 5]
dict4 = {}
for num in nums:
    dict4[num] = dict4.get(num, 0) + 1
print(dict4)    # {1: 1, 2: 2, 3: 2, 4: 2, 5: 1}



# =====================序列对象======================
colors = ['red','blue','green'] # colors = ('red','blue','green') # colors = "abcde"
# 1. 序列对象（string,list,tuple）遍历，序列可迭代
for color in colors:
    print(color)    # red blue green

# 2. 遍历倒序，反转遍历
for color in reversed(colors):
    print(color)    # green blue red

# 3. 同时遍历两个序列，zip()返回迭代器
numOfColors = [1,2,3]
colors = ['red','blue','green']
for num, color in zip(numOfColors, colors):
    print(num, '-->', color)    # 1 --> red     2 --> blue      3 --> green

# 4. 遍历排序的序列，sorted(, reverse=True)返回降序的新序列  ！！！默认升序排序
colors = ['red','blue','green']
for color in sorted(colors, reverse=True):
    print(color)    # red green blue

# 5. 自定义排序，key=len 比较长度排序，或自定义函数处理
colors = ['yellow','red','blue','green']
print(sorted(colors,key=len))   # ['red', 'blue', 'green', 'yellow']

# 6. 展开序列，展开的个数对应序列元素的个数！
a, b, c, d = colors
print(a, b, c, d)

# 7. 更新序列，collections模块里面的双向队列
import collections
colors = collections.deque(['yellow','red','blue','green'])
colors.popleft()
colors.appendleft('test')
print(colors)   # deque(['test', 'red', 'blue', 'green'])



# =====================类型转换======================
# 1. 元组转字典
tuple2list = ((1, 'a'), (2, 'b'))  # <class 'tuple'>
tuple2list_res = {x[0] : x[1] for x in tuple2list}
print(tuple2list_res)  # {1: 'a', 2: 'b'}

# 2. 列表转字典
list2dict = ['a', 'bb', 'ccc']
list2dict_res = {index : value for index, value in enumerate(list2dict)}
print(list2dict_res)    # {0: 'a', 1: 'bb', 2: 'ccc'}


# =====================输出======================
# 1. 类似三目运算输出
a = 2
print('ok' if a==1 else 'ko')   # ko



# =====================判断======================
# 1. 直接return条件判断
def test(m):
    return 'a' if m == 1 else 'b'

# 2. 带条件的推导列表
print([x for x in range(10) if x%2==0]) # [0, 2, 4, 6, 8]
print([x for x in range(30) if x%2==0 and x%3==0])  # [0, 6, 12, 18, 24]
print([x+1 if x>5 else x*10 for x in range(10)])    # [0, 10, 20, 30, 40, 50, 7, 8, 9, 10]



# =====================排序======================
# 1. 排序
import heapq
num=[10,2,9,22,111]
print(heapq.nlargest(3, num))   # [111, 22, 10]
print(heapq.nsmallest(3, num))  # [2, 9, 10]

student = [{'names':'CC','height':189},
           {'names':'BB','height':169},
           {'names':'AA','height':199}]
print(heapq.nsmallest(2,student,key=lambda x:x['height']))  # [{'names': 'BB', 'height': 169}, {'names': 'CC', 'height': 189}]



# =====================查找======================
# 1. 查询
list_for_serach = ['to_haha', 'recorde', 'test']
res_starts = filter(lambda x:x.startswith('te'), list_for_serach) #过滤器
resList_starts = [one_res for one_res in res_starts]
print(resList_starts)  # ['test']

# 2. 正则匹配
import re
res_re = filter(lambda x:re.findall(u'to_',x),list_for_serach) #re正则
resList_re = [one_res for one_res in res_re]
print(resList_re) # ['to_haha']

# 3. 函数遍历多出口问题，for else 结构
def find(seq, target):
    for key,value in enumerate(seq):
        if value == target:
            break
    else:
        return -1
    return key

## 遍历文件遇到指定字符退出
# better 偏函数partial()
# blocks = []
# if block in iter(partial(read, 32), ''):
#     blocks.append(block)



# =====================其他======================
# 1. 交换变量
a, b = 0, 1
a, b = b, a
print(a, b)
