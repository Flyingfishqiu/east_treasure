# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TreasureItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    time = scrapy.Field()
    name = scrapy.Field()
    ranking = scrapy.Field()
    code = scrapy.Field()

    top = scrapy.Field()
    plate = scrapy.Field()
    # link = scrapy.Field()
    day_open = scrapy.Field()
    highest = scrapy.Field()
    lowest = scrapy.Field()
    VOL = scrapy.Field()
    total = scrapy.Field()
    circulatio = scrapy.Field()
    shiying = scrapy.Field()
    shijing = scrapy.Field()
    zljl = scrapy.Field()
    day_5 = scrapy.Field()
    day_10 = scrapy.Field()

