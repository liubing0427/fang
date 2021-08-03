# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()

    # 链接地址
    link = scrapy.Field()

    # 标题
    title = scrapy.Field()

    # 小区的名字
    xiaoqu = scrapy.Field()

    # 区域
    region = scrapy.Field()

    # 几室几厅
    rooms = scrapy.Field()

    # 建筑面积
    area = scrapy.Field()

    # 朝向
    toward = scrapy.Field()

    # 层
    floor = scrapy.Field()

    # 年代
    year = scrapy.Field()

    # 总价
    price = scrapy.Field()

    # 单价
    unit = scrapy.Field()

    # 标签
    tag = scrapy.Field()

    # 最后一次扫描时间
    last_time = scrapy.Field()
