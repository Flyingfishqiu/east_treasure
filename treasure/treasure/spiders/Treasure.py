# -*- coding: utf-8 -*-
import scrapy
from treasure.items import TreasureItem

class TreasureSpider(scrapy.Spider):
    name = 'Treasure'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://data.eastmoney.com/zjlx/list.html']

    def parse(self, response):
        item = TreasureItem()

        tr_list = response.xpath('//*[@id="dt_1"]/tbody/tr')
        print("-------------------------")
        print(tr_list)

        print('+++++++++++++++++++++++')
        for tr in tr_list:
            item['code'] = tr.xpath('./td[2]/a/text()').extract_first()
            item['name'] = tr.xpath('./td[3]/a/text()').extract_first()
            item['top'] = tr.xpath('./td[7]/span/text()').extract_first()
            item['plate'] = tr.xpath('./td[15]/a/text()').extract_first()
            item['link'] = tr.xpath('./td[4]/a[2]/@href').extract_first()

            yield scrapy.Request(item['link'], callback=self.detile_parse, meta={'treasure_item':item})

    #
    # VOL': '-',
 # 'circulatio': '-',
 # 'code': '603008',
 # 'day_10': None,
 # 'day_5': None,
 # 'day_open': '-',
 # 'highest': '-',
 # 'link': 'http://data.eastmoney.com/stockdata/603008.html',
 # 'lowest': '-',
 # 'name': '喜临门',
 # 'plate': '木业家具',
 # 'shijing': '-',
 # 'shiying': '-',
 # 'top': '50',
 # 'total': '-',
 # 'zljl': None}

    def detile_parse(self, response):
        # http://data.eastmoney.com/stockdata/002940.html
        # 今开：40.19	最高：40.19	最低：40.19	成交量：391.00手
        # 总市值：36.17亿	流通市值：9.04亿	市盈：27.35	市净：4.00资金流：今日：主力净流入124万，主力排名1， 5日：主力净流入278万，主力排名1； 10日：主力净流入278万，主力排名1
        item = response.meta['treasure_item']
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
        # # 10日：主力净流入278万，主力排名1
        # // *[ @ id = "dl_headerZjl"] / dd[3] / label[1] / span / text()
        item['day_10'] = response.xpath('//*[@id="dl_headerZjl"]/dd[3]/label[1]/span/text()').extract_first()

        yield item