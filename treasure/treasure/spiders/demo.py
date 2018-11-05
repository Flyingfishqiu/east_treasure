# -*- coding: utf-8 -*-
import string

import scrapy
from treasure.items import TreasureItem
import re

import jsonpath

class TreasureSpider(scrapy.Spider):
    name = 'Treasure4'
    allowed_domains = ['eastmoney.com','dfcfw.com']
    # start_urls = ['http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(FFRank)&sr=1&p=1&ps=50&js=var%20tLxmodmJ={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51379400']
    p = 1
    bas_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(FFRank)&sr=1&p=' + str(
        p) + '&ps=50&js=var%20tLxmodmJ={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51379400'
    start_urls = [bas_url]

    def parse(self, response):
        item = {}

        # tr_list = response.xpath('//*[@id="dt_1"]/tbody/tr')
        # print("-------------------------")
        # print(tr_list)
        #
        # print('+++++++++++++++++++++++')
        # for tr in tr_list:
        #     item['code'] = tr.xpath('./td[2]/a/text()').extract_first()
        #     item['name'] = tr.xpath('./td[3]/a/text()').extract_first() #
        #     item['top'] = tr.xpath('./td[7]/span/text()').extract_first()
        #     item['plate'] = tr.xpath('./td[15]/a/text()').extract_first()
        #     item['link'] = tr.xpath('./td[4]/a[2]/@href').extract_first()#
        data_list = response.body.decode('utf-8').split('data:')[1].split('}</pre></body></html>')[0].strip(
            string.punctuation).split('","')
        for data in data_list:
            li = data.split(',')
            item['code'] = li[1]
            item['name'] = li[2]
            item['time'] = li[-1]
            item['ranking'] = li[5]
            print(item)
        # for data in data_list:
        #     li = data.split(',')
        #     item['name'] = li[2]
        #     item['time'] = li[-1]
        #     item['ranking'] = li[5]
        #     url = 'http://data.eastmoney.com/stockdata/{}.html'.format(li[1])
        #     # yield scrapy.Request(url, callback=self.detile_parse, meta={'treasure_item': item})

        self.p += 1
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(FFRank)&sr=1&p=' + str(
            self.p) + '&ps=50&js=var%20tLxmodmJ={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51379400'
        print("============================1===================================")
        print(self.p)
        print('hello')
        print('+++++++++++++++++++++++++++++++++++++100++++++++++++++++++++++++++++++++++++++')
        print(url)
        if self.p <3:
            yield scrapy.Request(url, callback=self.parse)
            print('==========================')