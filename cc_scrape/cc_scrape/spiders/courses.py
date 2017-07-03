# -*- coding: utf-7 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from cc_scrape.items import courseItem
from cc_scrape.items import deptItem

class courseSpider(scrapy.Spider):
    name = 'courses'
    start_urls = ['https://www.washington.edu/students/crscat/']
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, endpoint='render.html', args={'wait': 0.5})
    
    def parse(self, response):
        # follow links to courses
        dept = []
        link = response.xpath('//*[@id="uw-container-inner"]/div[2]/div/div[1]/ul/.//a[contains(@href, ".html")]')
        for href in link:
            dItem = deptItem()
            dItem['cname'] = href.xpath('.//text()').extract()
            dept.append(dItem)
            yield response.follow(href, callback=self.parse_course, meta={'cname': dItem, 'splash': {'endpoint': 'render.html', 'args': {'wait': 0.5}}, 'url': href.extract()})

    def parse_course(self, response):
        # get course details
        dItem = response.meta['cname']
        dItem['courses'] = []
        for x in response.xpath('/html/body/p/a[@name]'):
            cItem = courseItem()
            cItem['title'] = x.xpath('b/text()').extract()
            cItem['info'] = x.xpath('text()').extract()
            dItem['courses'].append(cItem)

        yield dItem

