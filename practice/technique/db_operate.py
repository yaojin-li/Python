"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 数据库相关操作
 1. 操作 MySQL
 2. 操作 Oracle
 3. 操作 MongoDB
 4. 导出 MySQL 数据至 excel
 5. 导出 Oracle 数据至 excel
 --------------------------------
 @Time    : 2019/6/7 15:45
 @File    : db_operate.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""


import re
import json
import cx_Oracle
import xlrd
from pathlib import Path
import pymysql
import time


def create_mysql_connect():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='123456789',
        db='page_log',
        port=3306,
        charset='utf8'
    )
    # 获得游标
    cur = conn.cursor()
    conn.autocommit(1)
    return cur, conn

def close_connect(conn):
    conn.commit()
    conn.close()



class Mysql():
    pass

class Oracle():
    pass

class Mongodb():
    pass


class Trans():
    def __init__(self):
        self.jsonPath = "json2mongo.json"
        self.mysqlPath = "csv2mysql.csv"
        self.oraclePath = "csv2oracle.csv"
        self.oracle_localhost = cx_Oracle.connect('app_common_service/Tebon@20180522@192.168.2.49:1521/orcl')    # 链接信息：localhost:1521/orcl，在数据库中右键属性，查看链接详细信息

    def csv2oracle(self):
        print("connect to oracle...")
        try:
            # 1. 链接Oracle数据库
            conn = self.oracle_localhost
            cursor = conn.cursor()

            # 2. 查询数据
            sql = "select * from KCB_INFO_AND_LISTED_INFO where row_count =1"
            cursor.execute(sql)
            allData = cursor.fetchall()  # cursor.fetchone()
            for data in allData:
                print(data)

            # # 3. 插入、更新、删除  主要区别在于sql不同
            # def sqlDML(sql, conn):
            #     cursor = conn.cursor()
            #     cursor.execute(sql)
            #     cursor.close()
            #     conn.commit()

            conn.commit()
            cursor.close()
            conn.close()
        except:
            conn.rollback()

trans = trans()
# trans.json2mongodb()
# trans.csv2mysql()
trans.csv2oracle()


