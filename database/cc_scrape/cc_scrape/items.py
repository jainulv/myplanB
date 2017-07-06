# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class courseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()

class deptItem(scrapy.Item):
    cname = scrapy.Field()
    courses = scrapy.Field()
