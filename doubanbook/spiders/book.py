# -*- coding: utf-8 -*-

import scrapy
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from doubanbook.items import DoubanbookItem

class doubanbookspider(CrawlSpider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/小说?start=0&type=T']
    # ruels = (
    #     Rule(LxmlLinkExtractor(allow=".*"), callback='parse'),
    #     Rule(LxmlLinkExtractor(allow=".*"), follow=True),
    # )

    # 分解出链接
    def parse(self, response):
        book_url = response.xpath('//h2/a/@href').extract()
        for url in book_url:
            yield scrapy.http.Request(url,  meta={'url': url}, callback=self.parse_data)

        nextpage = response.xpath('//*[@id="subject_list"]/div[2]/span[@class="next"]/a/@href').extract()
        if nextpage:
            url = u'https://book.douban.com'+nextpage[0]
            yield scrapy.http.Request(url, callback=self.parse)

    #获得数据
    def parse_data(self, response):
        item = DoubanbookItem()
        item['book_name'] =  response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()[0]
        item['auth_name'] = response.xpath('//*[@id="info"]/span[1]/a/text()').extract()[0]
        item['book_url'] = response.meta['url']
        item['pic_url'] = response.xpath('//*[@id="mainpic"]/a/img/@src').extract()[0]
        item['rate'] = response.xpath('//*[@id="interest_sectl"]/div/div[@class="rating_self clearfix"]/strong/text()').extract()[0]
        item['rate_num'] = response.xpath('//span[@property="v:votes"]/text()').extract()[0]
        print "----------- Current book:%s-----------" % item['book_name'].encode('gbk')
        yield item



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
