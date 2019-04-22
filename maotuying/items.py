# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaotuyingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site_name = scrapy.Field()
    site_url = scrapy.Field()

class MaotuyingReviewItem(scrapy.Item):
    review_site = scrapy.Field() 
    review_url = scrapy.Field()
    review_quote = scrapy.Field()
    review_detail = scrapy.Field()
    review_user = scrapy.Field()
    review_time = scrapy.Field()
#review_site,review_url,review_quote,review_detail,review_user,review_time