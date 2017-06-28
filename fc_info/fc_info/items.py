# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FcInfoItem(scrapy.Item):
    company_name = scrapy.Field()
    memberIds = scrapy.Field()
    name = scrapy.Field()
    source_url = scrapy.Field()
    medal = scrapy.Field()
    is_authentication = scrapy.Field()
    location = scrapy.Field()
    founding_time = scrapy.Field()
    inquiry_sheet = scrapy.Field()
    bidding = scrapy.Field()
    recruit_suppliers = scrapy.Field()
    purchase_amount = scrapy.Field()
    purchase_frequency = scrapy.Field()
    introduce = scrapy.Field()
    purchase_url = scrapy.Field()
    recruit_url = scrapy.Field()
    company_info_url = scrapy.Field()
    notice_url = scrapy.Field()
    pass
