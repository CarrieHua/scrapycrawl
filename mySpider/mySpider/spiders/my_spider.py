#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from mySpider.items import MyspiderItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MySpider(Spider):
    name = "mySpider"
    
    def start_requests(self):
        url = "https://bugzilla.mozilla.org/buglist.cgi?bug_status=UNCONFIRMED&bug_status=NEW&bug_status=ASSIGNED&bug_status=RESOLVED&bug_status=VERIFIED&bug_status=CLOSED&product=Firefox&query_format=advanced&resolution=---&resolution=FIXED&resolution=INVALID&resolution=WONTFIX&resolution=DUPLICATE&resolution=WORKSFORME&resolution=INCOMPLETE&resolution=SUPPORT&resolution=EXPIRED&resolution=MOVED&order=bug_status%2Cpriority%2Cbug_severity&limit=0"
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
         self.log('Hi, this is an item pages! %s' % response.url)
         item = MyspiderItem()
         #item['url'] = response.xpath('//td[@class="first-child bz_id_column"]/a/@href').extract()
         #print item['url']
         item['bug_id'] = response.xpath('//td[@class="first-child bz_id_column"]/a/text()').extract()
         return item


        
