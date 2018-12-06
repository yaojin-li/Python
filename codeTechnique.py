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
dict_zip = dict(zip('abcd', range(4)))  # zip()返回元组的列表，个数与最短的一致

# 2.1. 更新字典
dict1 = {'a': '1'}
dict2 = {'b': '2', 'c': '3'}
dictRes = dict(dict2, **dict1)  # 多参数添加字典
print(dictRes)  # {'b': '2', 'c': '3', 'a': '1'}

# 2.2. 更新字典
dict2.update(dict1)
print(dict2)  # {'b': '2', 'c': '3', 'a': '1'}

# 4. 字典循环
dict3 = {'1': 'a', '2331': 'b', '13': 'c'}
for key in dict3:
    print(key)
for key in dict3.keys():  # 只有当循环中需要更改key值的情况下，需要使用dict3.keys()
    if key.startswith('1'):
        print(dict3[key])

# 5. 用字典进行统计-合并同类项
nums = ['1', '22', '233', '4', '55']
from collections import defaultdict

dict5 = defaultdict(list)
for num in nums:
    key = len(num)
    dict5[key].append(num)
print(dict5)  # defaultdict(<class 'list'>, {1: ['1', '4'], 2: ['22', '55'], 3: ['233']})

# 6.1. 合并字典
dict6 = {'a': 1}
dict7 = {'b': 2}
dict6.update(dict7)
print(dict6)  # {'a': 1, 'b': 2}

# 6.2. 合并字典
dict6 = {'a': 1}
dict7 = {'b': 2}
print({**dict6, **dict7})  # {'a': 1, 'b': 2}

# 6.3. 合并字典  items() 以列表返回可遍历的元组数组
dict6 = {'a': 1}
dict7 = {'b': 2}
print(dict(dict6.items() | dict7.items()))  # {'a': 1, 'b': 2}

# 7.1. 通过值，排序字典元素
dict8 = {'a': 2, 'e': 3, 'f': 8, 'd': 4}
print(sorted(dict8, key=dict8.get))  # ['a', 'e', 'd', 'f']

# 7.2. 排序字典元素---lambda x:x[1] 返回列表的第二个元素(2,3,4,8)
dict9 = {'a': 2, 'e': 3, 'f': 8, 'd': 4}
print(sorted(dict9.items(), key=lambda x: x[0]))  # 根据键排序 [('a', 2), ('d', 4), ('e', 3), ('f', 8)]
print(sorted(dict9.items(), key=lambda x: x[1]))  # 根据值排序 [('a', 2), ('e', 3), ('d', 4), ('f', 8)]

# 8. 直接操作值
dict1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
double_dict = {key: value ** 2 for key, value in dict1.items()}
print(double_dict)  # {'a': 1, 'b': 4, 'c': 9, 'd': 16, 'e': 25}


# 9. 字典代替多个if else
def fun(x):
    if x == 'a':
        return 1
    elif x == 'b':
        return 2
    else:
        return None


def fun(x):
    print({"a": 1, "b": 2}.get(x))  # 字典的get()方法


# 10.


# =====================列表======================
# 1.1. 嵌套list转一个list
more2oneList = [1, [2, [3, 4]]]
resList = []


def fun(more2oneList):
    for i in more2oneList:
        if isinstance(i, list):
            fun(i)  # 递归
        else:
            resList.append(i)


fun(more2oneList)
print(resList)  # [1, 2, 3, 4]

# 1.2. 嵌套list转一个list
more2oneList_ = [[[1, 2], [100, 101], [3]], [[7, 8]]]
print([z for x in more2oneList_ for y in x for z in y])  # [1, 2, 100, 101, 3, 7, 8]

# 2. 统计列表元素个数
nums = [1, 2, 3, 4, 4, 3, 2, 5]
dict4 = {}
for num in nums:
    dict4[num] = dict4.get(num, 0) + 1
print(dict4)  # {1: 1, 2: 2, 3: 2, 4: 2, 5: 1}

# 3.1. 统计列表中频率最高的值---set()去重，max()取最大值，依据key是nums的个数
nums = [1, 2, 3, 4, 4, 3, 2, 5, 1, 1]
print(max(set(nums), key=nums.count))  # 1

# 3.2. 统计列表中频率最高的值---采用counter()方法取频率最高的值
from collections import Counter

nums = [1, 2, 3, 4, 4, 3, 2, 5, 1, 1]
nums_count = Counter(nums)
print(nums_count.most_common(len(nums)))  # [(1, 3), (2, 2), (3, 2), (4, 2), (5, 1)]

# 4. 序列对象连接（列表转字符串）
strList = ['1', '2', '3']
print(''.join(strList))  # 没有额外的内存分配

# 5.1. 反转列表---切片
numList = [1, 2, 4]
print(numList[::-1])  # [4, 2, 1]

# 5.2. 反转列表---reversed()
numList = [1, 2, 4]
for num in reversed(numList):
    print(num)  # 4 2 1

# 6. 列表最小值、最大值的索引---min(), max() --- __getitem__取值
min_max = [1, 3, 5, 10]
print("minIndex: ", min(range(len(min_max)), key=min_max.__getitem__))  # 0
print("maxIndex: ", max(range(len(min_max)), key=min_max.__getitem__))  # 3

# 7.1. 移除重复元素---set()
list_get_only = [1, 2, 3, 4, 4, 4, 2]
print(list(set(list_get_only)))  # [1, 2, 3, 4]

# 7.1. 移除重复元素---OrderedDict.fromkeys()
from collections import OrderedDict

list_get_only = [1, 2, 3, 4, 4, 4, 2]
print(list(OrderedDict.fromkeys(list_get_only).keys()))  # [1, 2, 3, 4]

# 8. 对相同位置的列表数据进行相加---map()返回迭代器
add_muti_list = list(map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6]))
print(add_muti_list)

# 9. 列表取值（高级拆包）
getConFromList = ['David', '22', '000', 'Pythonista', '123']
# Python 3 Only
first, *others = getConFromList
print(first, '---', *others)  # David --- 22 000 Pythonista 123
first, *middle, last = getConFromList
print(first, '---', *middle, '---', last)  # David --- 22 000 Pythonista --- 123

# 10. 遍历列表及索引
items = 'zero one two three'.split()
for index, value in enumerate(items):
    print(index, '-->', value)  # 0 --> zero    1 --> one    2 --> two    3 --> three

# 11. 同时访问多列表--循环嵌套
from itertools import product

x_list = [1, 2]
y_list = [3, 4]
z_list = [5, 6]
for x, y, z in product(x_list, y_list, z_list):
    print(x, y, z)  # 返回product()中，每个元素的笛卡尔积的元组
    # 1 3 5
    # 1 3 6
    # 1 4 5
    # 1 4 6
    # 2 3 5
    # 2 3 6
    # 2 4 5
    # 2 4 6

# =====================元组======================
# 1. 重组元组内容（不可改数据类型）
T = (1, 2, 3)
# T[1] = 4  # 无法修改
print(T[:2] + (4,))  # 切片 + 重组元组
print(T)  # 保持原来的内容不变

# 2. 拼接元组内容
T = ("3", "4", "1")
sum = ""
for char in T:
    sum += str(char)
print(int(sum), sum.__class__)

# =====================字符串======================
# 1. 检查两个字符串是不是由相同字母不同顺序组成
from collections import Counter

str1 = "123"
str2 = "321"
print(Counter(str1) == Counter(str2))  # Tureend

# 2.1. 反转字符串---切片
str2 = "123456789"
print(str[::-1])  # 987654321

# 2.2. 反转字符串---reversed()
str3 = "123456789"
for oneChar in reversed(str):
    print(''.join(oneChar))  # 987654321

# 3. 字符串格式化
str4 = "test"
print(f'{str4} just test!')  # test just test!

# =====================数组======================
# 1. 数组转置---zip()用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表
# 一个 * 传递位置参数（元组），两个 ** 传递关键字参数（字典）
array = [['a', 'b'], ['c', 'd'], ['e', 'f']]
print(list(zip(*array)))  # [('a', 'c', 'e'), ('b', 'd', 'f')]

# =====================数值======================
# 1. 反转数值
num_reversed = 123456789
print(int(str(num_reversed)[::-1]))

# =====================序列对象======================
colors = ['red', 'blue', 'green']  # colors = ('red','blue','green') # colors = "abcde"
# 1. 序列对象（string,list,tuple）遍历，序列可迭代
for color in colors:
    print(color)  # red blue green

# 2. 遍历倒序，反转遍历
for color in reversed(colors):
    print(color)  # green blue red

# 3. 同时遍历两个序列，zip()返回迭代器
numOfColors = [1, 2, 3]
colors = ['red', 'blue', 'green']
for num, color in zip(numOfColors, colors):
    print(num, '-->', color)  # 1 --> red     2 --> blue      3 --> green

# 4. 遍历排序的序列，sorted(, reverse=True)返回降序的新序列  ！！！默认升序排序
colors = ['red', 'blue', 'green']
for color in sorted(colors, reverse=True):
    print(color)  # red green blue

# 5. 自定义排序，key=len 比较长度排序，或自定义函数处理
colors = ['yellow', 'red', 'blue', 'green']
print(sorted(colors, key=len))  # ['red', 'blue', 'green', 'yellow']

# 6. 展开序列，展开的个数对应序列元素的个数！
a, b, c, d = colors
print(a, b, c, d)

# 7. 更新序列，collections模块里面的双向队列
import collections

colors = collections.deque(['yellow', 'red', 'blue', 'green'])
colors.popleft()
colors.appendleft('test')
print(colors)  # deque(['test', 'red', 'blue', 'green'])

# 8. 统计 defaultdict传入int，则可以用来计数：
import collections
from collections import defaultdict

T = (1, 2, 3, 2, 2, 2, 1, 4)  # 字符串，列表，元组
D = defaultdict(int)
for k in T:
    D[k] += 1
print(D.items())  # dict_items([(1, 2), (2, 4), (3, 1), (4, 1)])

# =====================类型转换======================
# 1. 元组转字典
tuple2list = ((1, 'a'), (2, 'b'))  # <class 'tuple'>
tuple2list_res = {x[0]: x[1] for x in tuple2list}
print(tuple2list_res)  # {1: 'a', 2: 'b'}

# 2. 列表转字典
list2dict = ['a', 'bb', 'ccc']
list2dict_res = {index: value for index, value in enumerate(list2dict)}
print(list2dict_res)  # {0: 'a', 1: 'bb', 2: 'ccc'}

# 3. 只有在数字类型中才存在类型转换
S = "42"
I = 1
X = S + I  # 类型错误 用意不明确，数字or字符串？
X = int(S) + I  # 做加法: 43
X = S + str(I)  # 字符串联接: "421"

# =====================输出======================
# 1. 类似三目运算输出
a = 2
print('ok' if a == 1 else 'ko')  # ko


# =====================判断======================
# 1. 直接return条件判断
def test(m):
    return 'a' if m == 1 else 'b'


# 2. 带条件的推导列表
print([x for x in range(10) if x % 2 == 0])  # [0, 2, 4, 6, 8]
print([x for x in range(30) if x % 2 == 0 and x % 3 == 0])  # [0, 6, 12, 18, 24]
print([x + 1 if x > 5 else x * 10 for x in range(10)])  # [0, 10, 20, 30, 40, 50, 7, 8, 9, 10]

# 3. 直接判断真伪
if x:
    pass
if items:
    pass

# 4. 判断对象类型--多个指定的类型
print(isinstance('a', (int, tuple)))  # False

# =====================排序======================
# 1. 排序
import heapq

num = [10, 2, 9, 22, 111]
print(heapq.nlargest(3, num))  # [111, 22, 10]
print(heapq.nsmallest(3, num))  # [2, 9, 10]

student = [{'names': 'CC', 'height': 189},
           {'names': 'BB', 'height': 169},
           {'names': 'AA', 'height': 199}]
print(heapq.nsmallest(2, student,
                      key=lambda x: x['height']))  # [{'names': 'BB', 'height': 169}, {'names': 'CC', 'height': 189}]

# =====================查找======================
# 1. 查询
list_for_serach = ['to_haha', 'recorde', 'test']
res_starts = filter(lambda x: x.startswith('te'), list_for_serach)  # 过滤器
resList_starts = [one_res for one_res in res_starts]
print(resList_starts)  # ['test']

# 2. 正则匹配
import re

res_re = filter(lambda x: re.findall(u'to_', x), list_for_serach)  # re正则
resList_re = [one_res for one_res in res_re]
print(resList_re)  # ['to_haha']


# 3. 函数遍历多出口问题，for else 结构
def find(seq, target):
    for key, value in enumerate(seq):
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


# =====================操作符======================
# 1. 操作符in
if fruit in ['apple', 'orange', 'berry']:
    pass

# =====================其他======================
# 1. 交换变量
a, b = 0, 1
a, b = b, a  # 先生成一个元组(tuple)对象，然后unpack
print(a, b)

# 2. 链式比较
c = 2
print(1 < c < 3)

# 3. 交互环境下的 "_" 操作符，"_" 是上一个执行的表达式的输出
# >>> 2 + 1
# 3
# >>> _
# 3

# 4. 使用any() / all()函数
# all()："有‘假’为False，全‘真’为True，iterable为空是True"
# any()："有‘真’为True，全‘假’为False，iterable为空是False"
##不推荐
found = False
for item in a_list:
    if condition(item):
        found = True
        break
if found:
    pass
    # do something if found...

##推荐
if any(condition(item) for item in a_list):
    pass
    # do something if found...



