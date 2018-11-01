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

            yield item

