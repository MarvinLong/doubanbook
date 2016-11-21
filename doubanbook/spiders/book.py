# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doubanbook.items import DoubanbookItem

class doubanbookspider(CrawlSpider):
    name = 'book'
    allowed_domains = ['book.douban.com/tag/']
    start_urls = ['http://book.douban.com/tag/文学?start=0&type=T']
    ruels = (
        Rule(LinkExtractor(allow=u'/tag/'), callback='parse_item', follow=True),
        #Rule(LinkExtractor(allow=u'/tag/科技/'), callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        item = DoubanbookItem()
        self.get_name(self, response, item)
        self.get_author(self, response, item)
        self.get_bookurl(self, response, item)
        self.get_picurl(self, response, item)
        self.get_rate(self, response, item)
        self.get_ratenum(self, response, item)
        return item

    def get_name(self, response, item):
        book_name = response.xpath('//h2/a/@title').extract()
        for book in book_name:
            # print "********Current book:%s************" % book
            item['book_name'] = book

    def get_author(self, response, item):
        author_name = response.xpath('//div[@class="pub"]/text()').extract()
        for author in author_name:
            item['author_name'] = author.replace('\n','').replace('  ', '')

    def get_bookurl(self, response, item):
        book_url = response.xpath('//h2/a/@href').extract()
        for url in book_url:
            item['book_url'] = url

    def get_picurl(self, response, item):
        pic_url = response.xpath('//div[@class="pic"]/a/img/@src').extract()
        for url in pic_url:
            item['pic_url'] = url

    def get_rate(self, response, item):
        rate = response.xpath('//span[@class="rating_nums"]/text()').extract()
        for r in rate:
            item['rate'] = r

    def get_ratenum(self, response, item):
        rate_nums = response.xpath('//div[@class="pub"]/text()').extract()
        for rate_num in rate_nums:
            item['rate_num'] = rate_num.replace('\n','').replace('  ', '')
