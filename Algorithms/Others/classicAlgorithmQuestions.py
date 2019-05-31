"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 基本经典算法
 1. 菲波拉契数列问题
 2. 判断素数问题
 3. 判断水仙花数问题
 4. 获取分数评级（嵌套条件运算符）
 5. 正整数分解质因数
 6. 最大公约数和最小公倍数
 7. 统计字符串内容
 8. 计算特殊表达式的和 求s=a+aa+aaa+aaaa+aa…a的值
 9. 判断一个数是否是完数（一个数如果恰好等于它的因子之和，如6=1＋2＋3）
 10.阶乘 求1+2!+3!+…+20!的和
 11.判断回文数
 12.四数取三，排列组合
 --------------------------------
 @Time    : 2018/11/26 20:30
 @File    : classicAlgorithmQuestions.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import math


######### 1. 菲波拉契数列问题 #########
class fibonacci(object):
    def __init__(self, num):
        self.num = num

    # 建立数组---空间复杂度高
    def getFibonacciList_three(self):
        result = []
        result.insert(0, 1)
        result.insert(1, 1)
        for i in range(2, self.num):
            result.insert(i, result[i - 1] + result[i - 2])
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


######### 2. 判断素数问题 #########
def isPrime(num):
    flag = True
    for i in range(2, int(math.sqrt(num) + 1)):  # <=， +1表示判断math.sqrt(num)这个数是否为素数
        if num % i == 0:
            flag = False
            break
    return flag


######### 3. 判断水仙花数 #########
def getDaffodil():
    beginNum = 101
    endNum = 1000
    for i in range(beginNum, endNum):
        a = int(i % 10)  # int()取整数，否则计算浮点数
        b = int(i / 10 % 10)
        c = int(i / 100)
        if a ** 3 + b ** 3 + c ** 3 == i:
            print(i)


######### 4. 获取分数评级（嵌套条件运算符）#########
def getScoreSign(score):
    return "A" if score >= 90 else "B" if score >= 60 else "C"


######### 5. 正整数分解质因数 #########
def getPrimeNum(num):
    n = 2
    result = []
    while num >= n:
        if num == n:
            result.append(num)  # ！找到最终的，也是最大的质因数
            break  # 退出循环
        elif num % n == 0:  # 说明此时的num可以再次被分解
            result.append(n)  # ！每次被n整除时，n均作为质因数，而不是num
            num = int(num / n)  # ！每次取整数
        else:
            n += 1  # ！n自增找到最大质因数本身。例如：7
    return result


######### 6. 最大公约数和最小公倍数 #########
# /*在循环中，只要除数不等于0，用较大数除以较小的数，
# 若两数相同，最大公约数为本身；
# 将小的一个数作为下一轮循环的大数，取得的余数作为下一轮循环的较小的数，
# 如此循环直到较小的数的值为0，
# 返回较大的数，此数即为最大公约数，最小公倍数为两数之积除以最大公约数。 /
def getMaxComDivisorAndMinComMultiple(num_one, num_two):
    # 判断大小数-设置num_two为大数
    if num_one > num_two:
        num_two, num_one = num_one, num_two
    while num_one != 0:
        if num_one == num_two:  # ！循环出口条件 两数相同，最大公约数为本身
            return num_two
        temp = num_one
        num_one = int(num_two % num_one)  # ！余数肯定比被除数小，将余数设为小的数
        num_two = temp
    return num_two


######### 7. 统计字符串内容 #########
# 输入一行字符，分别统计出其中 中文、英文字母、空格、数字和其它字符的个数
def countNum(string):
    result = [0, 0, 0, 0, 0]
    for char in string:
        if u'\u4e00' <= char <= u'\u9fa5':  # 判断是否是汉字，在isalpha()方法之前判断
            result[0] += 1
        elif char.isalpha():  # ！汉字也返回true
            result[1] += 1
        elif char.isspace():
            result[2] += 1
        elif char.isdigit():
            result[3] += 1
        else:
            result[4] += 1
    return result


######### 8. 计算特殊表达式的和 求s=a+aa+aaa+aaaa+aa…a的值 #########
def getNumSum(num, count):
    sum = 0
    result = 0
    for i in range(count):
        sum += num * 10 ** i
        result += sum
    print(result)
    return result


######### 9. 判断一个数是否是完数（一个数如果恰好等于它的因子之和，如6=1＋2＋3） #########
def isCompleteNum(num):
    sum = 0
    for i in range(1, int(num / 2) + 1):
        if num % i == 0:
            sum += i
    return True if sum == num else False


######### 10. 求1+2!+3!+…+20!的和 #########
def factorial(num):
    sum = 0
    temp = 1
    for one_num in range(1, num + 1):
        temp *= one_num
        sum += temp
    return sum


def factorial_two(num):
    from functools import reduce
    sum = 0
    for i in range(2, num + 2):  # 从2开始，num+2结束
        sum += reduce(lambda x, y: x * y, range(1, i))  # reduce() 累积
        print(sum)


######### 11. 判断一个数是否为回文数 #########
def isNumberOfTracts(num):
    if num < 0 or (num % 10 == 0 and num != 0):
        return False
    str1 = str(num)
    str2 = str(num)[::-1]  # 列表反转
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            print(str1[i], str2[i], "   error index is:", i)
            return False
    else:
        return True


######### 12. 四数取三，排列组合 #########
# 有1、2、3、4四个数字，能组成多少个互不相同且一个数字中无重复数字的三位数。不涉及0
# 字符串涉及重复内容。set()去重。
def permutations(num):
    count = 0
    for i in range(1, num + 1):
        for j in range(1, num + 1):
            for k in range(1, num + 1):
                if ((i != j) and (j != k) and (i != k)):
                    count += 1
                    print(i * 100 + j * 10 + k, i, j, k)
    print(count)


# itertools.combinations()组合；itertools.permutations()排列，列出所有可能性
def permutations_one(tar, num):
    '''
    :param tar: 待排列或组合的目标
    :param num: 选取个数
    :return: 排列或组合的结果
    '''
    import itertools
    permutations = itertools.permutations(str(tar), num)
    result = []
    for permutation in list(permutations):
        sum = ""
        for char in permutation:
            sum += str(char)
        if tar.__class__ is int:
            result.append(int(sum))
        else:
            result.append(sum)
    print(result)


if __name__ == '__main__':
    print(isNumberOfTracts(10))
    pass

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

    ######### 6. 最大公约数和最小公倍数 #########
    maxComDivisor = getMaxComDivisorAndMinComMultiple(200, 12)
    minComMultiple = int(200 * 12 / maxComDivisor)
    print(maxComDivisor, minComMultiple)
    
    ######### 7. 统计字符串内容 #########
    countNum("123test 哈哈 #@*")
    
    ######### 8. 计算特殊表达式的和 求s=a+aa+aaa+aaaa+aa…a的值 #########
    getNumSum(num=3, count=6)
    
    ######### 9. 判断一个数是否是完数（一个数如果恰好等于它的因子之和，如6=1＋2＋3） #########
    isCompleteNum(num=6)

    ######### 10. 求1+2!+3!+…+20!的和 #########
    factorial(20)

    ######### 11. 判断回文数 #########
    isNumberOfTracts(12345687654321)
    
    ######### 12. 四数取三，排列组合 #########
    permutations(4)
    permutations_one(1230, 3)
"""
