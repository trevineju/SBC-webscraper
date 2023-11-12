# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SBCitem(scrapy.Item):
    titulo = scrapy.Field()
    data = scrapy.Field()
    autoria = scrapy.Field()
    url = scrapy.Field()
    evento = scrapy.Field()
