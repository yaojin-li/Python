"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : python 技巧
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
## 快速构建字典
dict_zip = dict(zip('abcd', range(4)))

## 更新字典——1
dict1 = {'a':'1'}
dict2 = {'b':'2', 'c':'3'}
dictRes = dict(dict2, **dict1)  # 多参数添加字典
# print(dictRes)   # {'b': '2', 'c': '3', 'a': '1'}
## 更新字典——2
dict2.update(dict1)
# print(dict2) # {'b': '2', 'c': '3', 'a': '1'}



# =====================列表======================
## list
more2oneList = [1,[2,[3,4]]]
resList = []
def fun(more2oneList):
    for i in more2oneList:
        if isinstance(i,list):
            fun(i)  # 递归
        else:
            resList.append(i)
fun(more2oneList)
# print(resList)  # [1, 2, 3, 4]

more2oneList_ = [[[1,2],[100,101],[3]],[[7,8]]]
# print([z for x in more2oneList_ for y in x



# =====================序列对象======================
## 序列对象（string,list,tuple）遍历
colors = ['red','blue','green'] # colors = ('red','blue','green') # colors = "abcde"
# better 序列可迭代
for color in colors:
    print(color)

## 遍历倒序
# better 反转遍历
for color in reversed(colors):
    print(color)

## 同时遍历两个序列
numOfColors = [1,2,3]
colors = ['red','blue','green']
# better zip()返回迭代器
for num, color in zip(numOfColors, colors):
    print(num, '-->', color)

## 遍历排序的序列
colors = ['red','blue','green']
# better sorted()返回升序的新序列  ！！！
for color in sorted(colors, reverse=True):
    print(color)

## 自定义排序
colors = ['red','blue','green','yellow']
# better key=len 比较长度排序，或自定义函数处理
print(sorted(colors,key=len))



# =====================类型转换======================
## 元组转字典
tuple2list = ((1,'a'), (2,'b'))  # <class 'tuple'>
one_dic = {x[0]:x[1] for x in tuple2list}
# print(one_dic)  # {1: 'a', 2: 'b'}

## 列表转字典
list2dict = ['a','bb','ccc']
two_dic = {index:value for index,value in enumerate(list2dict)}



# =====================输出======================
## 类似三目运算输出
a=2
# print('ok' if a==1 else 'ko')   # ko



# =====================判断======================
## 直接return条件判断
def test(m):
    return 'a' if m==1 else 'b'

## 带条件的推导列表
# print([x for x in range(10) if x%2==0]) # [0, 2, 4, 6, 8]
# print([x for x in range(30) if x%2==0 and x%3==0])  # [0, 6, 12, 18, 24]
# print([x+1 if x>5 else x*10 for x in range(10)])    # [0, 10, 20, 30, 40, 50, 7, 8, 9, 10]



# =====================排序======================
## 排序
import heapq
num=[10,2,9,22,111]
# print(heapq.nlargest(3, num))   # [111, 22, 10]
# print(heapq.nsmallest(3, num))  # [2, 9, 10]

student = [{'names':'CC','height':189},
           {'names':'BB','height':169},
           {'names':'AA','height':199}]
# print(heapq.nsmallest(2,student,key=lambda x:x['height']))  # [{'names': 'BB', 'height': 169}, {'names': 'CC', 'height': 189}]



# =====================查找======================
## 查询
list_for_serach = ['to_haha', 'recorde', 'test']
res_starts = filter(lambda x:x.startswith('te'), list_for_serach) #过滤器
resList_starts = [one_res for one_res in res_starts]
# print(resList_starts)  # ['test']

## 正则匹配
import re
res_re = filter(lambda x:re.findall(u'to_',x),list_for_serach) #re正则
resList_re = [one_res for one_res in res_re]
# print(resList_re) # ['to_haha']

## 遍历文件遇到指定字符退出
# better 偏函数partial()
# blocks = []
# if block in iter(partial(read, 32), ''):
#     blocks.append(block)



