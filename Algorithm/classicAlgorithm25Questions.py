"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 25个经典算法
 1. 菲波拉契数列问题
 2. 判断素数问题
 3. 判断水仙花数问题
 4. 获取分数评级（嵌套条件运算符）
 5. 正整数分解质因数
 --------------------------------
 @Time    : 2018/11/26 20:30
 @File    : classicAlgorithm25Questions.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import math


######### 1. 菲波拉契数列问题 begin #########
class fibonacci():
    def __init__(self, num):
        self.num = num

    # 建立数组---空间复杂度高
    def getFibonacciList_three(self):
        result = []
        result.insert(0, 1)
        result.insert(1, 1)
        for i in range(2, self.num):
            result.insert(i, result[i-1] + result[i-2])
        print(result)

    # 直接打印---从下往上计算 时间复杂度O(n)
    def getFibonacciList_two(self):
        one, two = 1, 1
        print(one, two, end="\t")
        for i in range(2, self.num):
            three = one + two
            one, two = two, three
            print(three, end="\t")

# 递归--时间复杂度高
def getFibonacciList_one(num):
    if num in [0, 1]:
        return 1
    else:
        return getFibonacciList_one(num - 1) + getFibonacciList_one(num - 2)
######### 1. 菲波拉契数列问题 end #########


######### 2. 判断素数问题 end #########
def isPrime(num):
    flag = True
    for i in range(2, int(math.sqrt(num) + 1)):     # <=， +1表示判断math.sqrt(num)这个数是否为素数
        if num % i == 0:
            flag = False
            break
    return flag
######### 2. 判断素数问题 end #########


######### 3. 判断水仙花数 end #########
def getDaffodil():
    beginNum = 101
    endNum = 1000
    for i in range(beginNum, endNum):
        a = int(i%10)           # int()取整数，否则计算浮点数
        b = int(i/10%10)
        c = int(i/100)
        if a**3 + b**3 + c**3 == i:
            print(i)
######### 3. 判断水仙花数 end #########


######### 4. 获取分数评级（嵌套条件运算符）begin #########
def getScoreSign(score):
    return "A" if score >= 90 else "B" if score >= 60 else "C"
######### 4. 获取分数评级（嵌套条件运算符） end #########


######### 5. 正整数分解质因数 begin #########
def getPrimeNum(num):
    n = 2
    result = []
    while num >= n:
        if num == n:
            result.append(num)      # ！找到最终的，也是最大的质因数
            break                   # 退出循环
        elif num % n == 0:          # 说明此时的num可以再次被分解
            result.append(n)        # ！每次被n整除时，n均作为质因数，而不是num
            num = int(num/n)        # ！每次取整数
        else:
            n += 1                  # ！n自增找到最大质因数本身。例如：7
    return result
######### 5. 正整数分解质因数 end #########




if __name__ == '__main__':
    """
    ######### 1. 菲波拉契数列问题 #########
    num = 10
    fibonacci = fibonacci(num)
    for i in range(num):
        print(getFibonacciList_one(i), end="\t")
    fibonacci.getFibonacciList_two()
    fibonacci.getFibonacciList_three()

    ######### 2. isPrime #########
    beginNum, endNum = 101, 200
    count = 0
    for i in range(beginNum, endNum):
        if isPrime(i):
            count += 1
            print(i, end=" ")
    print("总数：", count)

    ######### 3. 判断水仙花数  #########
    getDaffodil()

    ######### 4. 获取分数评级（嵌套条件运算符-python无三目运算） #########
    score = 60
    getScoreSign(score)

    ######### 5. 正整数分解质因数 #########
    num = 12
    getPrimeNum(num)

"""

