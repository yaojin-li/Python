"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------------
 @Description : 数据库相关操作
 --------------------------------------
 @File        : DB_operation.py
 @Time        : 2018/8/25 12:28
 @Software    : PyCharm
 --------------------------------------
 @Author      : lixj
 @Contact     : lixj_zj@163.com
 --------------------------------------
"""

import re
import traceback
import json
from pymongo import MongoClient
import pymysql
import csv
import cx_Oracle

class trans():
    def __init__(self):
        self.jsonPath = "json2mongo.json"
        self.mysqlPath = "csv2mysql.csv"
        self.oraclePath = "csv2oracle.csv"
        self.mongodb_localhost = "mongodb://localhost:27017"    # 修改的host为locaohost，或具体的连接地址（在MongoDB安装目录bin下，输入cmd，输入mongo查看具体的连接信息）
        self.mysql_localhost = pymysql.connect(
                host = 'localhost',
                port = 3306,
                user = 'root',
                passwd = '123456789',
                db = 'demo',
                charset = 'utf8'    # utf8 not utf-8
            )
        self.oracle_localhost = cx_Oracle.connect('scott/123456789@localhost:1521/orcl')    # 链接信息：localhost:1521/orcl，在数据库中右键属性，查看链接详细信息

    def json2mongodb(self):
        print("begin process json...")
        try:
            # 1. 连接MongoDB
            conn = MongoClient(self.mongodb_localhost)
            db = conn.demo  # 连接数据库demo，没有自动创建
            demo_json = db.demo_json    # 使用demo_json集合，没有自动创建

            # 2. 插入数据
            # demo_json.insert([{"name":"lxj", "age":"18"}, {"sex":"man"}])

            # 3. 查找数据
            # one_json = demo_json.find_one({"name":"lxj"})

            # obj = demo_json.find_one()
            # obj_id = obj["_id"]     # ObjectId类型，直接根据ObjectId用于定向查找
            # print(demo_json.find_one({"_id": obj_id}))

            # 4. 修改数据
            # demo_json.update_one({"name":"lxj"}, {"$set":{"age":"20"}})

            # 5. 遍历数据
            # print(db.demo_json.count())
            # for i in demo_json.find():
            #     print(i)

            # 6. 删除数据
            # db.demo_json.remove()   # 全部删除

            # 7. 插入json文件
            # with open(self.jsonPath, "r", encoding="utf-8") as f:
            #     jsonFile = json.load(f)
            #     demo_json.insert(jsonFile)
        except:
            traceback.print_exception

    def csv2mysql(self):
        print("begin mysql...")
        try:
            # 1. 连接MySQL
            conn = self.mysql_localhost
            cursor = conn.cursor()
            # findall_sql = "select * from test"
            # cursor.execute(findall_sql)

            # 2. 查看数据
            # all_row = cursor.fetchall()
            # print(all_row)

            # 3. 插入数据
            # insert_sql = "insert into test values ('2','zz','7')"
            # cursor.execute(insert_sql)

            # 4. 修改数据
            # update_sql = "update test set age = '33' where name = 'aaa'"
            # cursor.execute(update_sql)

            # 5. 删除数据
            # delete_sql = "delete from test where age<10"
            # cursor.execute(delete_sql)

            # 6. 新建表
            # header = ['id', '主题', '用户ID', '用户名', '推荐力度', '评论时间', '评论标题', '评论内容']
            # createTable_sqll = """
            # CREATE TABLE IF NOT EXISTS`testtest` (
            #   `%s` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            #   `%s` varchar(128) DEFAULT NULL,
            #   `%s` varchar(128) DEFAULT NULL,
            #   `%s` varchar(128) DEFAULT NULL,
            #   `%s` varchar(30) DEFAULT NULL,
            #   `%s` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            #   `%s` varchar(500) DEFAULT NULL,
            #   `%s` varchar(65533) DEFAULT NULL
            # ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            # """ % (header[0], header[1], header[2], header[3], header[4], header[5], header[6], header[7])
            # cursor.execute(createTable_sqll)

            # 7. 写入csv文件--采用csv方式
            # utf-8_sig编码，去掉多余字符BOM（打开utf-8文件时开头的一个多余字符，用来声明编码信息）
            with open(self.mysqlPath, "r", encoding="utf-8_sig") as f:
                csv_reader = csv.reader(f)
                headers = next(csv_reader)
                headers[0] = "id"   # 当列名为空时替换

                # 0. 遍历csv文件中的数据
                # for rows in csv_reader:
                #     print(rows)

                # 1. 新建表
                createTable_sql = """
                CREATE TABLE IF NOT EXISTS`test2` (
                  `%s` INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                  `%s` varchar(128) DEFAULT NULL,
                  `%s` varchar(128) DEFAULT NULL,
                  `%s` varchar(128) DEFAULT NULL,
                  `%s` varchar(30) DEFAULT NULL,
                  `%s` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `%s` varchar(500) DEFAULT NULL,
                  `%s` text(65533) DEFAULT NULL,
                  `%s` varchar(30) DEFAULT NULL,
                  `%s` varchar(30) DEFAULT NULL,
                  `%s` varchar(50) DEFAULT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
                """ % (headers[0], headers[1], headers[2], headers[3], headers[4], headers[5], headers[6], headers[7], headers[8], headers[9], headers[10])
                # cursor.execute(createTable_sql)

                # 2. 插入数据--注意数据清洗
                for i,rows in enumerate(csv_reader):    # enumerate为python内置函数，用于既要遍历索引又要遍历元素

                    # 涉及数据清洗，对存入数据库的数据清洁度的要求较高，双引号影响数据插入
                    name = rows[3]
                    comment = rows[7]

                    # 数据清洗
                    name = name.replace("\'", "")
                    comment = comment.replace("\"", "").replace(".,", ".").replace(",,", ",").replace("..,", "..").replace(":,", ":")

                    insert_sql = """INSERT INTO test2 VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""" % (rows[0], "'" + rows[1] + "'", "'" + rows[2] + "'", "'" + name + "'", "'" + rows[4] + "'", "'" + rows[5] + "'", "'" + rows[6] + "'", "'" + comment + "'", "'" + rows[8] + "'", "'" + rows[9] + "'", "'" + rows[10] + "'")
                    # cursor.execute(insert_sql)    # 插入数据

            conn.commit()   # 提交
            cursor.close()
            conn.close()
        except:
            conn.rollback() # 发生错误则全部回滚
            traceback.print_exception

    def csv2oracle(self):
        print("connect to oracle...")
        try:
            # 1. 链接Oracle数据库
            conn = self.oracle_localhost
            cursor = conn.cursor()

            # 2. 查询数据
            sql = "select * from EMP"
            cursor.execute(sql)
            allData = cursor.fetchall()     # cursor.fetchone()
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
            traceback.print_exception

trans = trans()
# trans.json2mongodb()
# trans.csv2mysql()
# trans.csv2oracle()
