# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doubanbook.items import DoubanbookItem

class doubanbookspider(CrawlSpider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/文学']
    ruels = (
        Rule(SgmlLinkExtractor(allow="https://book.douban.com/subject/\d*/"), callback='parse'),
        Rule(SgmlLinkExtractor(allow="https://book.douban.com/tag/文学.*"), follow=True),
    )

    def parse(self, response):
        item = DoubanbookItem()
        book_name = self.get_name(response)
        author_name = self.get_author(response)
        # book_url = self.get_bookurl(response)
        pic_url = self.get_picurl(response)
        # rate = self.get_rate(response)
        # rate_num = self.get_ratenum(response)
        length = len(book_name)
        for i in range(length):
            print "----------- Current num:%d -----------" % i
            item['book_name'] = book_name[i]
            item['auth_name'] = author_name[i].replace('\n','').replace('  ', '')
            # item['book_url'] = book_url[i]
            item['pic_url'] = pic_url[i]
            # item['rate'] = rate[i]
            # item['rate_num'] = rate_num[i].replace('\n','').replace('  ', '')
            yield item

        # nextpage = response.xpath('//*[@id="subject_list"]/div[2]/span[@class="next"]/a/@href').extract()
        # if nextpage:
        #     url = u'https://book.douban.com'+nextpage[0]
        #     yield scrapy.http.Request(url, callback=self.parse)

    def get_name(self, response):
        book_name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()
        return book_name

    def get_author(self, response):
        author_name = response.xpath('//*[@id="info"]/span[1]/a/text()').extract()
        return author_name

    def get_picurl(self, response):
        pic_url = response.xpath('//*[@id="mainpic"]/a/img/@src').extract()
        return pic_url

    ## 直接在tag页面下检测
    # def get_name(self, response):
    #     book_name = response.xpath('//h2/a/@title').extract()
    #     return book_name
    #
    # def get_author(self, response):
    #     author_name = response.xpath('//div[@class="pub"]/text()').extract()
    #     return author_name
    #
    # def get_bookurl(self, response):
    #     book_url = response.xpath('//h2/a/@href').extract()
    #     return book_url
    #
    # def get_picurl(self, response):
    #     pic_url = response.xpath('//div[@class="pic"]/a/img/@src').extract()
    #     return pic_url
    #
    # def get_rate(self, response):
    #     rate = response.xpath('//span[@class="rating_nums"]/text()').extract()
    #     '//*[@id="subject_list"]/ul/li[20]/div[2]/div[2]/span[2]'
    #     return rate
    #
    # def get_ratenum(self, response):
    #     rate_nums = response.xpath('//span[@class="pl"]/text()').extract()
    #     return rate_nums
