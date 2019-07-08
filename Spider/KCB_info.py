"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 爬取上交所科创版所有企业的相关信息
 --------------------------------
 @Time    : 2019/6/23 16:44
 @File    : dynamic_info.py
 @Software: PyCharm
 --------------------------------
 @Author  : lixj
 @contact : lixj_zj@163.com
"""

from lxml import etree
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
import os
from bs4 import BeautifulSoup
import requests


class Dynamic():
    def __init__(self):
        self.MAX_COL_NUM = 11  # 总列数
        self.SPECIAL_COL = [1, 9, 10]  # 特殊的列
        self.JSON_FILE_NAME = "doc/dynamic_info/dynamic_info.json"
        self.ROOT_PATH = "doc/info_details"
        self.COMPANY_INFO_DETAIL = "company_info_detail.txt"
        self.DISCLOSURE_INFO_FILE = "disclosure_info.json"
        self.BASIC_INFO_FILE = "basic_info.json"

        # 构造内容参考页面源代码
        self.PUBLISH_REPORT = {"30": "招股说明书", "36": "发行保荐书", "37": "上市保荐书", "32": "审计报告", "33": "法律意见书", "34": "其他"}
        self.PUBLISH_TYPE = ["申报稿", "上会稿", "注册稿"]

    def dynamic_info_result(self, html):
        """
        解析项目基本信息
        :param html: 解析页面 http://kcb.sse.com.cn/renewal/ 的 html
                     将解析结果 json 写入文件 self.JSON_FILE_NAME
        :return:
        """
        struct = etree.HTML(html)

        # 表头信息xpath
        default_rank = '//*[@id="defaultRank"]/text()'  # 序号
        stock_issuer = '//*[@id="stockIssuer"]/text()'  # 发行人全称
        curr_status = '//*[@id="currStatus"]/text()'  # 审核状态
        stock_issuer_province = '//*[@id="stockIssuer[0].s_province"]/text()'  # 注册地
        stock_issuer_code_desc = '//*[@id="stockIssuer[0].s_csrcCodeDesc"]/text()'  # 证监会行业
        intermediary = '//*[@id="intermediary"]/text()'  # 保荐机构，律师事务所，会计师事务所
        update_date = '//*[@id="updateDate"]/div[1]/text()'  # 更新日期
        audit_apply_date = '//*[@id="auditApplyDate"]/div[1]/text()'  # 受理日期

        # 提取表头信息
        head = struct.xpath(default_rank)
        stock_issuer = struct.xpath(stock_issuer)
        curr_status = struct.xpath(curr_status)
        stock_issuer_province = struct.xpath(stock_issuer_province)
        stock_issuer_code_desc = struct.xpath(stock_issuer_code_desc)
        intermediary = struct.xpath(intermediary)
        update_date = struct.xpath(update_date)
        audit_apply_date = struct.xpath(audit_apply_date)

        # 构建表头list
        title_list = [head[0], stock_issuer[0], curr_status[0], stock_issuer_province[0], stock_issuer_code_desc[0],
                      intermediary[0], intermediary[1], intermediary[2], update_date[0], audit_apply_date[0]]

        # 项目动态结果集
        res = []

        # 每个项目对应的项目信息详情页url结果集
        url_list = []

        # 公司名称结果集
        company_list = []

        # 获取所有tr
        trs = struct.xpath('//*[@id="dataList1_container"]/tbody/tr')

        # 遍历所有trs
        for i in range(2, len(trs) + 1):
            temp_dict = {}
            for j in range(1, self.MAX_COL_NUM):
                # 序号、更新日期、受理日期等内容读取td[]/text()，其他读取td[]/a/text()
                if j in self.SPECIAL_COL:
                    temp_url = '//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[' + str(j) + ']/text()'
                else:
                    temp_url = '//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[' + str(j) + ']/a/text()'
                temp_cont = struct.xpath(temp_url)

                # 当有表格中单元格的内容有多个字段时，拼接内容
                one_temp_con = ""
                if len(temp_cont) > 1:
                    for part in temp_cont:
                        one_temp_con += part
                else:
                    one_temp_con = temp_cont[0]
                temp_dict[title_list[j - 1]] = one_temp_con
            res.append(temp_dict)

            # 构建项目信息详情结果集
            one_url_list = struct.xpath('//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[2]/a/@href')
            one_company_list = struct.xpath('//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[2]/a/text()')
            url_list.append("http://kcb.sse.com.cn" + one_url_list[0])
            company_list.append(one_company_list[0])

        # 解析成json格式
        result = str(res).replace("'", "\"")

        # 存储json结果
        write_html(self.JSON_FILE_NAME, result)

        return url_list, company_list

    def basic_info_analysis(self, html, company_name):
        """
        解析项目基本信息表格，并下载下载表格内容至 basic_info_json
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'lxml')
        ths_list = []
        tds_list = []

        # 解析表格的 th，构造 key
        for th in soup.find_all("th", limit=14):
            ths_list.append(str.strip(th.string))
        # 解析表格的 td，构造value
        for td in soup.find_all("td", limit=14):
            tds_list.append(str.strip(td.string))
        basic_info = []
        # 构造完整的表格解析结果
        basic_info.append(dict(zip(ths_list, tds_list)))

        # 解析成json格式
        result = str(basic_info).replace("'", "\"")

        # 写入基本信息至 self.BASIC_INFO_FILE
        file_path = self.ROOT_PATH + os.altsep + company_name[0] + os.altsep + self.BASIC_INFO_FILE
        write_html(file_path, result)

    def pdf_download(self, company_name, title, url):
        """
        下载pdf文件
        :param company_name: 公司名称
        :param title: 文件标题
        :param url: 文件下载链接
        :return:
        """
        file_path = self.ROOT_PATH + os.altsep + company_name[0]

        # 判断文件路径是否存在
        if not os.path.exists(file_path):
            os.makedirs(self.ROOT_PATH + title)
        else:
            print("{}，路径存在！".format(file_path))
            req = requests.get(url, stream=True)
            with open(file_path + "/" + title + ".pdf", "wb") as f:
                for content in req.iter_content():
                    f.write(content)
            print("下载 {} 完成！".format(title))

    def disclosure_info_analysis(self, html, company_name):
        """
        解析信息披露表格，并下载对应的披露文件
        :param html:
        :return:
        """
        struct = etree.HTML(html)

        # 记录信息披露表格内容
        publish_info = {}
        for report_key in self.PUBLISH_REPORT.keys():
            # 记录每份披露文件信息
            report = {}
            for type_key, type_value in enumerate(self.PUBLISH_TYPE):
                # 每个披露文件对应的三种信息
                one_publish_info = {}
                time = struct.xpath('//*[@id="tile' + report_key + '"]/td[' + str(type_key + 1) + ']/a/text()')
                # 不存在 time，默认为 '-'
                if len(time) == 0:
                    one_publish_info['url'] = '-'
                    one_publish_info['time'] = '-'
                    one_publish_info['title'] = '-'
                else:
                    url = struct.xpath('//*[@id="tile' + report_key + '"]/td[' + str(type_key + 1) + ']/a/@href')
                    title = struct.xpath('//*[@id="tile' + report_key + '"]/td[' + str(type_key + 1) + ']/a/@title')
                    one_publish_info['time'] = time[0]
                    one_publish_info['url'] = url[0]
                    one_publish_info['title'] = title[0]

                    # 下载 pdf 文件
                    self.pdf_download(company_name, title[0], url[0])

                report[type_value] = one_publish_info
            publish_info[self.PUBLISH_REPORT[report_key]] = report

        result = str(publish_info).replace("'", "\"")

        # 写入信息披露至 self.DISCLOSURE_INFO_FILE
        file_path = self.ROOT_PATH + os.altsep + company_name[0] + os.altsep + self.DISCLOSURE_INFO_FILE
        write_html(file_path, result)

    def info_details_result(self, company_list):
        """
        解析每个公司的详细信息，仅包括项目基本信息表与信息披露表；
        暂不包括 问询与回复、上市委会议公告与结果、注册结果通知 三个表
        :param company_list: 公司名称列表
        :return: 
        """
        for company in company_list:
            html = read_html(self.ROOT_PATH + os.altsep + str(company) + os.altsep + self.COMPANY_INFO_DETAIL)

            struct = etree.HTML(html)
            company_name = struct.xpath('//*[@id="issuer_full_title"]/text()')

            # 解析项目基本信息表格
            self.basic_info_analysis(html, company_name)

            # 解析信息披露表格
            self.disclosure_info_analysis(html, company_name)

    def per_company_detail_html(self, url_list):
        """
        构造每个公司的文件夹并生成对应公司的详情文件
        :param url_list: 公司名称列表
        :return:
        """
        for url in url_list:
            async def get_content():
                browser = await launch({
                    'headless': True,
                })
                page = await browser.newPage()
                await page.goto(url)
                doc = pq(await page.content())
                struct = etree.HTML(str(doc))
                title = struct.xpath('//*[@id="issuer_full_title"]/text()')
                file_path = self.ROOT_PATH + os.altsep + title[0]
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                else:
                    print("{} 路径存在！".format(file_path))
                write_html(file_path + os.altsep + self.COMPANY_INFO_DETAIL, str(doc))
                await browser.close()

            asyncio.get_event_loop().run_until_complete(get_content())


def read_html(file):
    with open(file, "r", encoding="utf-8") as f:
        html = f.read()
    return html


def write_html(file, content):
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)
    print("写入 {} 完成！".format(file))


if __name__ == '__main__':
    # 1. 打开网页 http://kcb.sse.com.cn/renewal/
    # 2. F12 -> Source -> kcb.see.com.cn -> renewal -> (index)
    # 3. 359 行左右：
    #     container.getDataByAjax(url, utils.mergeJson(params,p),getNum);
    # 4. 在这一行打断点，改变 params 中的 pageHelp.pageSize 参数，继续运行
    # 5. 页面列表会加载所有科创版公司的相关信息
    # 6. 在 Elements 中选中 <html> 标签，右键 copy -> copy outerHTML，获取当前页所有展示的 html
    # 7. 文件结构：
    #    doc
    #    -- dynamic_info
    #       -- dynamic_info_html.txt    写入第 6 步的 html 内容
    #    -- info_details
    #    dynamic_info.py

    html = read_html("doc/dynamic_info/dynamic_info_html.txt")

    dynamic = Dynamic()
    # 获取每个公司的项目详情页url列表
    url_list, company_list = dynamic.dynamic_info_result(html)

    # 构造每个公司的文件夹并生成对应公司的详情文件；取前三个公司下载
    dynamic.per_company_detail_html(url_list[:3])

    # 解析每个公司的详细信息，仅包括项目基本信息表与信息披露表；
    # 暂不包括 问询与回复、上市委会议公告与结果、注册结果通知 三个表；取前三个公司下载
    dynamic.info_details_result(company_list[:3])
