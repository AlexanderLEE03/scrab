# -*- coding: utf-8 -*-
import scrapy
from zimuku.items import ZimukuItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['zimuku.net']
    start_urls = ['http://zimuku.net/']

    def parse(self, response):
        # pass
        items = {}
        for i in range(5):
            name = response.xpath('//td[@class = "first"]/a[@target = "_blank"]/@title').extract()[i]

            items['{}'.format(i)] = name
        return items
