# -*- coding: utf-8 -*-

'''
编写爬虫，进行解析，将数据存入item，在piplines文件中作为后续的处理。
'''

import scrapy
from scrapy.selector import Selector    # Selector: XPath selectors based on lxml
from douban_movie.items import DoubanMoiveItem

class DemoSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['douban_movie.io']     # 域名定义可省略

    def start_requests(self):
        urls = ['https://movie.douban.com/subject/1292052/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # parse()用于处理响应，解析内容形成字典；发现新的URL爬取请求
    def parse(self, response):
        sel = Selector(response)
        item = DoubanMoiveItem()
        item['name'] = sel.xpath('//*[@id="content"]/h1/span[1]/text()').extract()
        item['year'] = sel.xpath('//span[@property="v:initialReleaseDate"]/text()').extract()
        item['score'] = sel.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract()
        item['director'] = sel.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
        item['classification'] = sel.xpath('//span[@property="v:genre"]/text()').extract()
        item['actor'] = sel.xpath('//span[@class="attrs"]/a[@rel="v:starring"]/text()').extract()

        return item
