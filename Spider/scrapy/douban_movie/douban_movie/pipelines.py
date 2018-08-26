# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
pipelines文件中进行数据处理：
清洗HTML数据
验证解析到的数据（检查项目是否包含必要的字段）
检查是否是重复数据（如果重复就删除）
将解析到的数据存储到数据库中或写入到特定的文件中
'''

class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        print("爬取结果为...")
        print(item)

        with open("douban_movie.txt", 'w', encoding="utf-8") as f:
            f.write(str(item))

        # return item
