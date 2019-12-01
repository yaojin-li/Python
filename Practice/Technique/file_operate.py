"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 文件相关常用操作
 1. 获取指定目录及其子目录下，所有指定后缀的文件的绝对路径
 2. 遍历指定目录下（不包含子目录）所有文件，更新指定后缀
 3. 判断指定文件是否是指定后缀的文件
 4. 获取当前文件路径
 5. 获取目录层级
 6. 组合文件路径
 7. 流式分块读取大文件

 注：os 模块；path 模块；pathlib 库（重点）；
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


def get_suffix_file_path(dir_path, suffix):
    """
    获取指定目录及其子目录下，所有指定后缀的文件的绝对路径
    :param dir_path: 指定目录 eg. "D:\\ZX\\temp"
    :param suffix: 指定后缀 eg. "txt"
    :return:
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if str(file).endswith(suffix):
                file_list.append(os.path.join(root, file))
    return file_list


def rename_file_suffix(dir_path, old_suffix, new_suffix):
    """
    遍历指定目录下（不包含子目录）所有文件，更新指定后缀
    :param dir_path: 指定路径 eg. "F:\\temp"
    :param old_suffix: 待修改后缀 eg. "txt"
    :param new_suffix: 新后缀 eg. "jpg"
    :return:
    """
    for file_path in Path(dir_path).glob('*.' + old_suffix):
        file_path.rename(file_path.with_suffix("." + new_suffix))


def is_suffix_file(file, suffix):
    """
    判断指定文件是否是指定后缀的文件
    :param file: 指定文件 eg. "F:\\temp\\img.txt" or "demo.txt"
    :param suffix: 指定后缀 eg. "txt"
    :return: True or False
    """
    return pathlib.PurePath(file).match('*.' + suffix)


def get_current_working_directory():
    """
    获取当前文件路径
    :return:
    """
    print(os.path.dirname(__file__))
    print(os.getcwd())
    print(pathlib.Path.cwd())


def get_upper_two_levels():
    """
    获取目录层级 -- 获取上上层目录
    :return:
    """
    print(os.path.dirname(os.path.dirname(os.getcwd())))
    print(pathlib.Path.cwd().parent.parent)


def combined_path():
    """
    获取目录层级 -- 在上上层目录下拼接路径
    :return: 拼接结果
    """
    # os 模块
    print(os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "1", "2", "3"))

    # Path 模块
    parts = ["1", "2", "3"]
    print(pathlib.Path.cwd().parent.parent.joinpath(*parts))


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

    # pathlib 模块，封装了 with open() 方法
    Path(file_name).read_text()


def read_big_file_by_line():
    """
    流式逐行读取大文件（常规做法）
    :return:
    """
    # with 上下文管理器会自动关闭打开的文件描述符
    # 在迭代文件对象时，内容是一行一行返回的，不会占用太多内存
    # 缺点：大文本只有一行，所有内容读入内存
    with open("foo.txt") as f:
        for line in f:
            print(line)


def read_big_file_by_chunk(file_path):
    """
    流式分块读取大文件
    :param file_path: 文件路径
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
