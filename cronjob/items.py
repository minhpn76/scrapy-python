# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CronjobItem(scrapy.Item):
    # define the fields for your item here like:
    job_id = scrapy.Field()
    job_title = scrapy.Field()
    area1 = scrapy.Field()
    employment_type = scrapy.Field()
    job_category = scrapy.Field()
    salary_range = scrapy.Field()
    posted_date = scrapy.Field()
    age = scrapy.Field()
    requirements = scrapy.Field()
    salary = scrapy.Field()
    period = scrapy.Field()
    working_hour = scrapy.Field()
    location = scrapy.Field()
    desc = scrapy.Field()
    company_name = scrapy.Field()
    company_website = scrapy.Field()
    representative = scrapy.Field()
    email = scrapy.Field()
    tel = scrapy.Field()
    fax = scrapy.Field()
    pr = scrapy.Field()
