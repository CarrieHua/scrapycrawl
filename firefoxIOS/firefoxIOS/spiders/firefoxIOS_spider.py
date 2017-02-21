#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-


from scrapy.spiders import Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from firefoxIOS.items import FirefoxiosItem 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class FirefoxiosSpider(Spider):
    name = "firefoxIOS"
    allowed_domains = ["bugzilla.mozilla.org"]
    start_urls = ["https://bugzilla.mozilla.org/buglist.cgi?product=Firefox%20for%20iOS&query_format=advanced&resolution=---&resolution=FIXED&resolution=INVALID&resolution=WONTFIX&resolution=DUPLICATE&resolution=WORKSFORME&resolution=INCOMPLETE&resolution=SUPPORT&resolution=EXPIRED&resolution=MOVED&order=bug_status%2Cpriority%2Cbug_severity&limit=0"]
    rules = (
            Rule(LinkExtractor(allow = ('^https://bugzilla\.mozilla\.org/buglist\.cgi\?product=Firefox%20for%20iOS&query_format=advanced&resolution=---&resolution=FIXED&resolution=INVALID&resolution=WONTFIX&resolution=DUPLICATE&resolution=WORKSFORME&resolution=INCOMPLETE&resolution=SUPPORT&resolution=EXPIRED&resolution=MOVED&order=bug_status%2Cpriority%2Cbug_severity&limit=0$',)), follow = True),
            #select the htmls which contain the bugs that we need
            Rule(LinkExtractor(allow = ('^https://bugzilla\.mozilla\.org/show_bug\.cgi\?id=[0-9]{7}',)), callback = 'parse'),
            )

    def parse(self, response):
        self.log('Hi, this is an item pages! %s' % response.url)
        item = FirefoxiosItem()
        item['Status'] = response.xpath('//span[@id="static_bug_status"]/text()').extract()
        item['Product'] = response.xpath('//td[@id="field_container_product"]/text()').extract()
        item['Component'] = response.xpath('//td[@id="field_container_component"]/text()').extract()
        item['Platform'] = response.xpath('//tr/th/label[text()="Platform"]/../../td/text()').extract() 
        item['Version'] = response.xpath('//label[@for="version"]/text()').extract()
        item['Importance'] = response.xpath('//label[@for="priority"]/../../td/text()').extract() 
        item['AssignedTo'] = response.xpath('//tr/th/a[text()="Assigned To"]/../../td/text()').extract()
        item['TriageOwner'] = response.xpath('//tr/th/label[@for="triage_owner"]/../../td/span/span/text()').extract()
        item['Reported'] = response.xpath('//tr/th[text()="Reported:"]/../td/text()').extract()
        item['Reporter'] = response.xpath('//tr/th[text()="Reported:"]/../td/span/span/text()').extract()
        item['Modified'] = response.xpath('//tr/th[text()="Modified:"]/../td/text()').extract()
        item['CC'] = response.xpath('//tr/th/label[text()="Modified:"]/../../td/text()').extract()
        #item['Attachments'] = 
        item['Description'] = response.xpath('//div/div/span/a[text()="Description"]/../../../pre/text()').extract()
        item['Comments'] = response.xpath('//div[@class="bz_comment_head"]/../following-sibling::div/pre/text()').extract()
        return item


