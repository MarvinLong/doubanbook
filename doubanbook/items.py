# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    auth_name = scrapy.Field()
    pic_url = scrapy.Field()
    book_url = scrapy.Field()
    rate_num = scrapy.Field()
    rate = scrapy.Field()

