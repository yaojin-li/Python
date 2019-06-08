"""
 !/usr/bin/env python3.6
 -*- coding: utf-8 -*-
 --------------------------------
 Description : 爬取上交所科创版所有企业的相关信息
 --------------------------------
 @Time    : 2019/4/23 16:44
 @File    : dynamicInfo.py
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


def getDynamicInfoResult():
    """
    下载内容
    :return:
    """
    with open("doc/dynamicInfo/dynamicInfoHtml.text", "r", encoding="utf-8") as f:
        html = f.read()
    struct = etree.HTML(html)

    # 表头信息
    defaultRank = '//*[@id="defaultRank"]/text()'  # 序号
    stockIssuer = '//*[@id="stockIssuer"]/text()'  # 发行人全称
    currStatus = '//*[@id="currStatus"]/text()'  # 审核状态
    stockIssuerProvince = '//*[@id="stockIssuer[0].s_province"]/text()'  # 注册地
    stockIssuerCodeDesc = '//*[@id="stockIssuer[0].s_csrcCodeDesc"]/text()'  # 证监会行业
    intermediary = '//*[@id="intermediary"]/text()'  # 保荐机构，律师事务所，会计师事务所
    updateDate = '//*[@id="updateDate"]/div[1]/text()'  # 更新日期
    auditApplyDate = '//*[@id="auditApplyDate"]/div[1]/text()'  # 受理日期

    head = struct.xpath(defaultRank)
    stockIssuer = struct.xpath(stockIssuer)
    currStatus = struct.xpath(currStatus)
    stockIssuerProvince = struct.xpath(stockIssuerProvince)
    stockIssuerCodeDesc = struct.xpath(stockIssuerCodeDesc)
    intermediary = struct.xpath(intermediary)
    updateDate = struct.xpath(updateDate)
    auditApplyDate = struct.xpath(auditApplyDate)

    titleList = [head[0], stockIssuer[0], currStatus[0], stockIssuerProvince[0], stockIssuerCodeDesc[0],
                 intermediary[0], intermediary[1], intermediary[2], updateDate[0], auditApplyDate[0]]

    res = []  # 项目动态结果集
    urlList = []  # 每个项目对应的项目信息详情页url结果集
    companyList = []  # 公司名称结果集
    for i in range(2, 94):  # 94
        tempDict = {}
        for j in range(1, 11):  # 11
            if j in (1, 9, 10):  # 序号、更新日期、受理日期等内容读取td[]/text()，其他读取td[]/a/text()
                tempUrl = '//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[' + str(j) + ']/text()'
            else:
                tempUrl = '//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[' + str(j) + ']/a/text()'
            tempCont = struct.xpath(tempUrl)

            # 当有表格中单元格的内容有多个字段时，拼接内容
            oneTempCon = ""
            if len(tempCont) > 1:
                for part in tempCont:
                    oneTempCon += part
            else:
                oneTempCon = tempCont[0]
            tempDict[titleList[j - 1]] = oneTempCon
        res.append(tempDict)

        # 构建项目信息详情结果集
        oneUrlList = struct.xpath('//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[2]/a/@href')
        oneCompanyList = struct.xpath('//*[@id="dataList1_container"]/tbody/tr[' + str(i) + ']/td[2]/a/text()')
        urlList.append("http://kcb.sse.com.cn" + oneUrlList[0])
        companyList.append(oneCompanyList[0])

    # 解析成json格式
    result = str(res).replace("'", "\"")
    print(result)

    # 存储json结果
    with open("doc/dynamicInfo/dynamicInfo.json", "w", encoding="utf-8") as f:
        f.write(result)

    return urlList, companyList


def getInfoDetailsResult(companyList):
    """
    获取每家公司项目信息详情
    :return:
    """
    rootPath = "doc/infoDetails/"
    for company in companyList:
        with open(rootPath+ str(company)+"/companyInfoDetail.text", "r", encoding="utf-8") as f:
            html = f.read()

        ##  解析项目基本信息
        soup = BeautifulSoup(html, 'lxml')
        thsList = []
        tdsList = []
        for th in soup.find_all("th", limit=14):
            thsList.append(str.strip(th.string))
        for td in soup.find_all("td", limit=14):
            tdsList.append(str.strip(td.string))
        basicInfo = []
        basicInfo.append(dict(zip(thsList, tdsList)))
        print(basicInfo)

        ##  解析信息披露表格
        publishReport = {"30": "招股说明书", "36": "发行保荐书", "37": "上市保荐书", "32": "审计报告", "33": "法律意见书", "34": "其他"}
        publishType = ["申报稿", "上会稿", "注册稿"]
        struct = etree.HTML(html)
        companyName = struct.xpath('//*[@id="issuer_full_title"]/text()')
        publishInfo = {}  # 记录信息披露表格内容
        for reportKey in publishReport.keys():
            report = {}  # 记录每份披露文件信息
            for typeKey, typeValue in enumerate(publishType):
                onePublishInfo = {}  # 每个披露文件对应的三种信息
                time = struct.xpath('//*[@id="tile' + reportKey + '"]/td[' + str(typeKey + 1) + ']/a/text()')
                if len(time) == 0:
                    onePublishInfo['url'] = '-'
                    onePublishInfo['time'] = '-'
                    onePublishInfo['title'] = '-'
                else:
                    url = struct.xpath('//*[@id="tile' + reportKey + '"]/td[' + str(typeKey + 1) + ']/a/@href')
                    title = struct.xpath('//*[@id="tile' + reportKey + '"]/td[' + str(typeKey + 1) + ']/a/@title')
                    onePublishInfo['url'] = url[0]
                    onePublishInfo['time'] = time[0]
                    onePublishInfo['title'] = title[0]

                    ## 下载pdf文件
                    if not os.path.exists(rootPath + companyName[0]):
                        os.makedirs(rootPath + title[0])
                    else:
                        print(rootPath + companyName[0] + "路径存在")
                        re = requests.get(url[0], stream=True)
                        with open(rootPath + companyName[0] + "/" + title[0] + ".pdf", "wb") as f:
                            for content in re.iter_content():
                                f.write(content)
                        print("下载" + title[0] + "完成")

                report[typeValue] = onePublishInfo
            publishInfo[publishReport[reportKey]] = report

        result = str(publishInfo).replace("'", "\"")
        print(result)


if __name__ == '__main__':
    # async def getDynamicInfoHtml():
    #     """
    #     抓取所有企业项目动态（需手动在网页接口获取数据中，增加所有的企业）
    #     :return:
    #     """
    #     browser = await launch()
    #     page = await browser.newPage()
    #     await page.goto('http://kcb.sse.com.cn/renewal/',timeout=0)
    #     doc = pq(await page.content())
    #     with open("doc/dynamicInfo/dynamicInfoHtml.text", "w", encoding="utf-8") as f:
    #         f.write(str(doc))
    #     await browser.close()
    # asyncio.get_event_loop().run_until_complete(getDynamicInfoHtml())

    ## sleep()等待

    ## 更新stock_list div 中的内容

    ## 获取每个公司的项目详情页url列表
    urlList, companyList = getDynamicInfoResult()

    # 针对前五家公司，构造每个公司的文件夹并生成对应公司的详情html
    for url in urlList[:5]:
        async def getCompanyInfoDetailHtml():
            browser = await launch({
                'headless': False,
                # 代理ip
                'args': ['--proxy-server=114.230.234.120:31594',]
            })
            page = await browser.newPage()
            await page.goto(url)
            doc = pq(await page.content())
            struct = etree.HTML(str(doc))
            title = struct.xpath('//*[@id="issuer_full_title"]/text()')
            rootPath = "doc/infoDetails/"
            if not os.path.exists(rootPath + title[0]):
                os.makedirs(rootPath + title[0])
            else:
                print(rootPath + title[0] + "路径存在")
            with open("doc/infoDetails/" + title[0] + "/companyInfoDetail.text", "w+", encoding="utf-8") as f:
                f.write(str(doc))
            await browser.close()
        asyncio.get_event_loop().run_until_complete(getCompanyInfoDetailHtml())

    ##
    getInfoDetailsResult(companyList[:5])
