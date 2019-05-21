"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 测试 apscheduler
 使用：
 1.安装pyinstaller包、pywin32包；
 2.同目录下，存放xx.ico图标文件；
 3.pycharm的terminal中执行打包指令：
   >pyinstaller -F -w -i a.ico testApscheduler.py
 4.生成对应的testApscheduler.exe文件

 参考链接：
 https://www.jianshu.com/p/4f5305e220f0
 https://zhuanlan.zhihu.com/p/46948464
 --------------------------------
 @Time    : 2019/5/21 10:50
 @File    : testApscheduler.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

from multiprocessing import freeze_support
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def tick():
    with open("aa.txt", "w", encoding="utf-8") as f:
        f.write("123456")
        print("write done")


if __name__ == '__main__':
    freeze_support()  # 防止多进程
    scheduler = BlockingScheduler()
    # 通过CronTrigger设置时间，防止pyinstall打包执行exe报错：No trigger by the name "cron" was found
    trigger = CronTrigger(hour='15', minute='55')
    scheduler.add_job(tick, trigger=trigger)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
