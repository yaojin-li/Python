"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : zip 文件常用操作
 --------------------------------
 @Time    : 2019/8/13 15:24
 @File    : test_zip.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

import zipfile
import os

def unzip_file(zip_file_name, unzip_path):
    """
    解压 zip 文件。（注：解压文件路径下包含同名称待解压文件，会覆盖！）
    :param zip_file_name: 解压文件的名称，含路径全地址
    :param dic_path: 解压文件路径
    """
    if zipfile.is_zipfile(zip_file_name):
        archive = zipfile.ZipFile(zip_file_name, mode='r')
        for file in archive.namelist():
            archive.extract(file, unzip_path)
    else:
        print("{} is not zip file.".format(zip_file_name))


def get_zip_file_name(dic_path):
    """
    将指定的 zip 文件内容解压到指定路径中
    :param dic_path: 指定路径
    :return: 压缩文件全路径
    """
    zip_file_path = []
    for root, dirs, files in os.walk(dic_path):
        for file in files:
            if os.path.splitext(file)[1] == '.zip':  # 读取zip文件
                zip_file_path.append(os.path.join(root, file))
    return zip_file_path


if __name__ == '__main__':
    zip_file_path = "E:\\zip"  # zip file 路径
    upzip_file_path = "E:\\zip\\res"  # 解压路径

    fn = get_zip_file_name(zip_file_path)
    for file in fn:
        unzip_file(file, upzip_file_path)
        
