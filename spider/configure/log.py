"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 
 --------------------------------------
 @File        : log.py
 @Time        : 2019/2/28 22:31
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

# -*- coding:utf-8 -*-
import logging
import logging.config
import os

path = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(path))

debug_flag = True

# 给过滤器使用的判断
class RequireDebugTrue(logging.Filter):
    # 实现filter方法
    def filter(self, record):
        return debug_flag

logging_config = {
    #必选项，其值是一个整数值，表示配置格式的版本，当前唯一可用的值就是1
    'version': 1,
    # 是否禁用现有的记录器
    'disable_existing_loggers': False,

    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': RequireDebugTrue,   #在开发环境，我设置DEBUG为True；在客户端，我设置DEBUG为False。从而控制是否需要使用某些处理器。
        }
    },

    #日志格式集合
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },

    # 处理器集合
    'handlers': {
        # 输出到控制台
        'console': {
            'level': 'DEBUG',  # 输出信息的最低级别
            'class': 'logging.StreamHandler',
            'formatter': 'simple',  # 使用standard格式
            'filters': ['require_debug_true', ],  # 仅当 DEBUG = True 该处理器才生效
        },
        # 输出到文件
        'log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(BASE_DIR, 'debug.log'),  # 输出位置
            'maxBytes': 1024 * 1024 * 5,  # 文件大小 5M
            'backupCount': 5,  # 备份份数
            'encoding': 'utf8',  # 文件编码
        },
    },

    # 日志管理器集合
    'loggers':{
        'root': {
            'handlers': ['console','log'],
            'level': 'DEBUG',
            'propagate': True,  # 是否传递给父记录器
        },
        'simple': {
            'handlers': ['console','log'],
            'level': 'WARN',
            'propagate': True,  # 是否传递给父记录器,
        }
    }
}
