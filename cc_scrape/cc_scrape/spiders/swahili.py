# -*- coding: utf-7 -*-
import scrapy
from scrapy.selector import Selector
from cc_scrape.items import CcScrapeItem
from scrapy_splash import SplashRequest

class SwahiliSpider(scrapy.Spider):
    name = 'swahili'
    allowed_domains = ['www.washington.edu']
    start_urls = ['https://www.washington.edu/students/crscat/swa.html']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 0.5})

    def parse(self, response):
        for x in response.xpath('/html/body/p/a[@name]'):
            yield {
                    'title': x.xpath('b/text()').extract(),
                    'info': x.xpath('text()').extract()
            }
