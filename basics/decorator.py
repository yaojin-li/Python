"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 装饰器常见用法
 参考网址：https://mp.weixin.qq.com/s/8z92pbhJV1ybfE6YZfvOuw?scene=25#wechat_redirect
 --------------------------------
 @Time    : 2019/8/14 14:10
 @File    : decorator.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import time


## 1. 简单 demo
def decorator(func):
    """
    定义装饰器。调用含有该装饰器的函数时，先将这个函数做为参数传入该装饰器。
    :param func: 含有该装饰器的函数
    :return:
    """

    def wrapper(*args, **kwargs):
        return func()

    return wrapper


@decorator
def function():
    print("hello decorator")


## 2. 日志打印装饰器
def logger(func):
    def wrapper(*args, **kwargs):
        print("开始执行：{}函数".format(func.__name__))
        # 真正执行
        func(*args, **kwargs)
        print("执行：{}函数完毕".format(func.__name__))

    return wrapper


@logger
def add(x, y):
    print("{}+{}={}".format(x, y, x + y))


## 3. 时间计时器
def timer(func):
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        # 执行函数
        func(*args, **kwargs)
        cost_time = time.time() - begin_time
        print("程序耗时：{}秒".format(cost_time))

    return wrapper


@timer
def test_timer_sleep(sleep_time):
    time.sleep(sleep_time)


## 4. 带参数的函数装饰器--两层嵌套
def say_hello(contry):
    def wrapper(func):
        def deco(*args, **kwargs):
            if contry == "china":
                print("你好！")
            elif contry == "america":
                print("hello.")
            else:
                return
            # 真正执行函数
            func(*args, **kwargs)

        return deco

    return wrapper


@say_hello("china")
def xiaoming():
    pass


@say_hello("america")
def jack():
    pass


## 5. 高阶：不带参数的类装饰器
# 基于类装饰器的实现，必须实现 __call__ 和 __init__两个内置函数。
# __init__ ：接收被装饰函数
# __call__ ：实现装饰逻辑。
class Logger(object):
    def __init__(self, func):
        # 接收被装饰函数
        self.func = func

    def __call__(self, *args, **kwargs):
        # 实现装饰逻辑
        print("[INFO]: the function {}() is running...".format(self.func.__name__))
        # 真正执行函数
        return self.func(*args, **kwargs)


@Logger
def say_no_parameter(something):
    print("say {}!".format(something))


## 6.高阶：带参数的类装饰器
# 带参数和不带参数的类装饰器有很大的不同。
# __init__ ：不再接收被装饰函数，而是接收传入参数。
# __call__ ：接收被装饰函数，实现装饰逻辑。
class Logger(object):
    def __init__(self, level='INFO'):
        # 接收参数
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # 实现装饰逻辑
            print("[{}]: the function {}() is running...".format(self.level, func.__name__))
            # 接收被装饰函数，执行函数
            func(*args, **kwargs)

        # 返回函数
        return wrapper


@Logger(level='WARNNING')
def say_with_parameter(something):
    print("say {}!".format(something))


## 7. 使用偏函数与类实现装饰器
# Python 对某个对象是否能通过装饰器（ @decorator）形式使用只有一个要求：
#   decorator 必须是一个 “可被调用” （callable）的对象。
# 对于这个 callable 对象，我们最熟悉的就是函数了。
# 除函数之外，类也可以是 callable 对象，只要实现了__call__ 函数（上面几个例子已经接触过了）。
# 还有容易被人忽略的偏函数其实也是 callable 对象。
import time
import functools


class DelayFunc:
    def __init__(self, duration, func):
        self.duration = duration
        self.func = func  # @delay(duration=2) 装饰器修饰的 add_partial() 函数

    def __call__(self, *args, **kwargs):
        print(f'Wait for {self.duration} seconds...')
        time.sleep(self.duration)
        return self.func(*args, **kwargs)


def delay(duration):
    """
    装饰器：推迟某个函数的执行。
    :param duration: 延迟时间
    :return: 执行结果
    """
    # 此处为了避免定义额外函数，直接使用 functools.partial 帮助构造 DelayFunc 实例
    return functools.partial(DelayFunc, duration)


# duration=2，延迟2秒
@delay(duration=2)
def add_partial(a, b):
    return a + b


## 8. 如何写能装饰类的装饰器？
# 单例模式---装饰器实现控制生成类实例
# 可以看到我们用 singleton 这个装饰函数来装饰 User 这个类。
# 装饰器用在类上，并不是很常见，但只要熟悉装饰器的实现过程，就不难以实现对类的装饰。

# 类的实例字典，key: 实例名称，value: 实例 object
instances = {}


def singleton(cls):
    """
    单例模式生成类
    :param cls: singleton 装饰器修饰的类
    :return:
    """

    def get_instance(*args, **kw):
        cls_name = cls.__name__
        if not cls_name in instances:
            # 生成装饰器修饰的类的实例
            instance = cls(*args, **kw)
            # 将实例加到字典中。key: cls_name，value: instance
            instances[cls_name] = instance
        # 返回该类的实例
        return instances[cls_name]

    return get_instance


@singleton
class User:
    def __init__(self, name):
        self.name = name


## 9. wraps 装饰器
# functools 标准库中有提供一个 wraps 装饰器
# 作用就是将 被修饰的函数(wrapped) 的一些属性值赋值给 修饰器函数(wrapper) ，最终让属性的显示更符合我们的直觉。
# 准确点说，wraps 其实是一个偏函数对象（partial）
from functools import update_wrapper

WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')


def wrapper(func):
    def inner_function():
        pass

    update_wrapper(inner_function, func, assigned=WRAPPER_ASSIGNMENTS)
    return inner_function


@wrapper
def wrapped():
    pass


print(wrapped.__name__)  # wrapped


## 10. 内置装饰器：property
# 内建装饰器，它通常存在于类中，可以将一个函数定义成一个属性，属性的值就是该函数return的内容。
# 用@property装饰过的函数，会将一个函数定义成一个属性，属性的值就是该函数return的内容。同时，会将这个函数变成另外一个装饰器。
# property 的底层实现机制是「描述符」
class TestProperty(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        print("in __get__")
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError
        return self.fget(obj)

    def __set__(self, obj, value):
        print("in __set__")
        if self.fset is None:
            raise AttributeError
        self.fset(obj, value)

    def __delete__(self, obj):
        print("in __delete__")
        if self.fdel is None:
            raise AttributeError
        self.fdel(obj)

    def getter(self, fget):
        print("in getter")
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        print("in setter")
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        print("in deleter")
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Student:
    def __init__(self, name):
        self.name = name

    # 其实只有这里改变
    @TestProperty
    def math(self):
        return self._math

    @math.setter
    def math(self, value):
        if 0 <= value <= 100:
            self._math = value
        else:
            raise ValueError("Valid value must be in [0, 100]")


# 说明：
# 1. 使用TestProperty装饰后，math 不再是一个函数，而是TestProperty类的一个实例。
# 所以第二个math函数可以使用 math.setter 来装饰，本质是调用TestProperty.setter 来产生一个新的 TestProperty 实例赋值给第二个math。
# 2. 第一个 math 和第二个 math 是两个不同 TestProperty 实例。但他们都属于同一个描述符类（TestProperty），
# 当对 math 对于赋值时，就会进入 TestProperty.__set__，
# 当对 math 进行取值里，就会进入 TestProperty.__get__。
# 仔细一看，其实最终访问的还是 Student 实例的 _math 属性。


# 运行后，会直接打印这一行，这是在实例化 TestProperty 并赋值给第二个math
# in setter
# >>>
# >>> s1.math = 90
# in __set__
# >>> s1.math
# in __get__
# 90


## 11. 其他装饰器：装饰器实战
# 一个实现控制函数运行超时的装饰器。如果超时，则会抛出超时异常。
import signal


class TimeoutException(Exception):
    def __init__(self, error='Timeout waiting for response from Cloud'):
        Exception.__init__(self, error)


def timeout_limit(timeout_time):
    def wraps(func):
        def handler(signum, frame):
            raise TimeoutException()

        def deco(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout_time)
            func(*args, **kwargs)
            signal.alarm(0)

        return deco

    return wraps


if __name__ == '__main__':
    # function()
    # add(1, 2)
    # test_timer_sleep(3)

    # xiaoming()
    # jack()

    # say_no_parameter("123")
    # say_with_parameter("456")

    ## 7. 偏函数
    # add_partial(1, 2)
    # >>> add_partial    # 可见 add 变成了 Delay 的实例
    # <__main__.DelayFunc object at 0x107bd0be0>
    #
    # >>> add_partial(3,5)  # 直接调用实例，进入 __call__
    # Wait for 2 seconds...
    # 8
    #
    # >>> add_partial.func # 实现实例方法
    # <function add_partial at 0x107bef1e0>

    ## 8. 单例模式
    # user_one = User("tony")
    # print(user_one)

    ## 9. wraps 装饰器
    # wrapped()

    ## 10. 内置装饰器：property
    pass
