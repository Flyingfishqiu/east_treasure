# -*- coding: utf-8 -*-
import string

import scrapy
from treasure.items import TreasureItem
import re


class TreasureSpider(scrapy.Spider):
    name = 'Treasure'
    allowed_domains = ['eastmoney.com','dfcfw.com']
    # start_urls = ['http://data.eastmoney.com/zjlx/list.html']
    p = 1
    bas_url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(FFRank)&sr=1&p='+str(p)+'&ps=50&js=var%20tLxmodmJ={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51379400'
    start_urls = [bas_url]

    def parse(self, response):
        item = TreasureItem()

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

            url = 'http://data.eastmoney.com/stockdata/{}.html'.format(li[1])
            yield scrapy.Request(url, callback=self.detile_parse, meta={'treasure_item':item,'data':li})

        self.p += 1
        url = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=ct&st=(FFRank)&sr=1&p='+str(self.p)+'&ps=50&js=var%20tLxmodmJ={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM&rt=51379400'
        print("============================1===================================")
        print(self.p)
        print('hello')
        print('+++++++++++++++++++++++++++++++++++++100++++++++++++++++++++++++++++++++++++++')
        if self.p <=4:
            yield scrapy.Request(url, callback=self.parse)



    def detile_parse(self, response):
        # http://data.eastmoney.com/stockdata/002940.html
        # 今开：40.19	最高：40.19	最低：40.19	成交量：391.00手
        # 总市值：36.17亿	流通市值：9.04亿	市盈：27.35	市净：4.00资金流：今日：主力净流入124万，主力排名1， 5日：主力净流入278万，主力排名1； 10日：主力净流入278万，主力排名1
        data = response.meta['data']

        item = response.meta['treasure_item']

        item['code'] = data[1]
        item['time'] = data[-1]
        item['ranking'] = data[5]
        item['name'] = response.xpath('//*[@id="name"]/text()').extract_first()
        # 今开
        # // *[ @ id = "gt1"] / text()
        item['day_open'] = response.xpath("//*[@id='gt1']/text()").extract_first()
        # # 最高
        # // *[ @ id = "gt2"] / text()
        item['highest'] = response.xpath("//*[@id='gt2']/text()").extract_first()
        # # 最低
        # // *[ @ id = "gt3"] / text()
        item['lowest'] = response.xpath("//*[@id='gt3']/text()").extract_first()
        # # 成交量
        # // *[ @ id = "gt4"] / text()
        item['VOL'] = response.xpath("//*[@id='gt4']/text()").extract_first()
        # # 总市值
        # // *[ @ id = "gt5"] / text()
        item['total'] = response.xpath("//*[@id='gt5']/text()").extract_first()
        # # 流通市值
        # // *[ @ id = "gt6"] / text()
        item['circulatio'] = response.xpath("//*[@id='gt6']/text()").extract_first()
        # # 市盈
        # // *[ @ id = "gt7"] / text()
        item['shiying'] = response.xpath("//*[@id='gt7']/text()").extract_first()
        # # 市净
        # // *[ @ id = "gt8"] / text()
        item['shijing'] = response.xpath("//*[@id='gt8']/text()").extract_first()
        # # 今日：主力净流入124万
        # // *[ @ id = "dl_headerZjl"] / dd[1] / label[1] / span / text()
        item['zljl'] = response.xpath('//*[@id="dl_headerZjl"]/dd[1]/label[1]/span/text()').extract_first()
        # #  5日：主力净流入278万，主力排名1；
        # // *[ @ id = "dl_headerZjl"] / dd[2] / label[1] / span / text()

        item['day_5'] = response.xpath('//*[@id="dl_headerZjl"]/dd[2]/label[1]/span/text()').extract_first()
        # 今日主力排名
        #     # //*[@id="dl_headerZjl"]/dd[2]/label[2]/text()

        # # 10日：主力净流入278万，主力排名1
        # // *[ @ id = "dl_headerZjl"] / dd[3] / label[1] / span / text()
        item['day_10'] = response.xpath('//*[@id="dl_headerZjl"]/dd[3]/label[1]/span/text()').extract_first()
        # 所属行业
        item['plate'] = response.xpath('//*[@id="bk1"]/text()').extract_first()
        yield item