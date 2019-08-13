"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 文件相关常用操作
 os 模块；
 path 模块；
 使用 pathlib 库（重点）；
 --------------------------------
 @Time    : 2019/5/25 22:28
 @File    : file_operate.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import os
from pathlib import Path
import pathlib
import os.path
from functools import partial

def getSameEndsFileInDir(fileDir, endStr):
    """
    遍历文件夹下所有后缀为endStr的文件，获取同一目录下所有文件的绝对路径
    :param fileDir:
    :return:
    """
    fileList = []
    for root, dirs, files in os.walk(fileDir):
        for filePath in files:
            if str(filePath).endswith(endStr):
                fileList.append(os.path.join(root, filePath))
    return fileList
   
   
def rename_file_suffix(dic_path, old_suffix, new_suffix):
    """
    遍历指定路径下所有文件，更新指定后缀
    :param dic_path: 指定路径
    :param old_suffix: 需要修改的文件后缀
    :param new_suffix: 新后缀
    :return:
    """
    for file_path in Path(dic_path).glob('*.' + old_suffix):
        file_path.rename(file_path.with_suffix("." + new_suffix))


def is_py_file():
    """
    判断当前文件是否符合 '*.py'规则的文件
    :return: True or False
    """
    return pathlib.PurePath(__file__).match('*.py')


def is_suffix_file(file_name, suffix):
    """
    判断指定文件是否是符合指定后缀的文件
    :param file_name: 文件名
    :param suffix: 指定后缀
    :return: True or False
    """
    return pathlib.PurePath(file_name).match('*.' + suffix)


def combined_path():
    """
    在上上层目录下拼接路径
    :return: 拼接结果
    """
    # return os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "1", "2", "3")
    parts = ["1", "2", "3"]
    return pathlib.Path.cwd().parent.parent.joinpath(*parts)


def get_current_working_directory():
    """
    获取当前文件路径
    """
    print(os.path.dirname(__file__))
    print(os.getcwd())
    print(pathlib.Path.cwd())


def get_upper_two_levels():
    """
    获取上上层目录
    """
    print(os.path.dirname(os.path.dirname(os.getcwd())))
    print(pathlib.Path.cwd().parent.parent)     
     
     
def get_file_path():
    """
    组合文件路径
    :return:
    """
    # 旧方法
    print(os.path.join('/temp', 'foo.txt'))
    # output: '/temp/foo.txt'

    # 新方法
    print(Path('/temp') / 'foo.txt')


def read_file(file_name):
    """
    快速读取文件
    :param file_name: 文件名
    :return:
    """
    # 标准做法
    with open(file_name) as f:
        f.read()

    # pathlib 模块
    Path(file_name).read_text()


def read_big_file_by_line():
    """
    流式逐行读取大文件（常规做法）
    :return:
    """
    # with 上下文管理器会自动关闭打开的文件描述符
    # 在迭代文件对象时，内容是一行一行返回的，不会占用太多内存
    # 缺点：大文本只有一行
    with open("foo.txt") as f:
        for line in f:
            print(line)


def read_big_file_by_chunk(file_path):
    """
    流式分块读取大文件
    :param file_name:
    :return:
    """
    # 普通做法
    with open(file_path) as file:
            for chunk in chunked_file_reader(file):
                yield chunk

    # 优秀做法
    with open(file_path) as file:
        for chunk in chunked_file_reader_mod(file):
            yield chunk

        
def chunked_file_reader(file, block_size=1024 * 8):
    """
    流式分块读取大文件（普通做法）
    :param file: 文件名，即 with open(file_name) as file:
    :param block_size: 分块大小
    :return:
    """
    while True:
        chunk = file.read(block_size)
        if not chunk:
            break
        yield chunk


def chunked_file_reader_mod(file, block_size=1024 * 8):
    """
    流式分块读取大文件（优秀做法）
    :param file: 文件名，with open(file_name) as file:
    :param block_size: 分块大小
    :return:
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的偏函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    for chunk in iter(partial(file.read, block_size), ''):
        yield chunk


if __name__ == '__main__':
    file_path = "../demo.txt"
    print(list(read_big_file_by_chunk(file_path)))

   
   
   
