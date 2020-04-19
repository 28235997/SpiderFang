# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouse(scrapy.Item):
    #省份
    province = scrapy.Field()
    #城市
    city = scrapy.Field()

    #小区名
    name = scrapy.Field()
    #价格
    price = scrapy.Field()
    #几居室
    rooms = scrapy.Field()
    #面积
    area = scrapy.Field()
    #地址
    address = scrapy.Field()
    #行政区
    district = scrapy.Field()
    #方天下详细页面的url
    origin_url = scrapy.Field()

class EsfHouse(scrapy.Item):
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 几居室
    rooms = scrapy.Field()
    #层
    floor = scrapy.Field()
    #朝向
    toward = scrapy.Field()
    #年代
    year = scrapy.Field()
    #面积
    area = scrapy.Field()
    #价格
    price = scrapy.Field()
    #地址
    address = scrapy.Field()
    #单价
    oneprice = scrapy.Field()
    #优势
    advantage = scrapy.Field()
    #小区名
    name = scrapy.Field()
