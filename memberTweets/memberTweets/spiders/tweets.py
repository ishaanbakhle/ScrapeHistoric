# -*- coding: utf-8 -*-
import scrapy
import pandas as pd

data = pd.read_csv("/Users/ishaanbakhle/Desktop/Projects/MemberStatements/memberTwitter/MemberHandles.csv")
handles = list(data["Handle"])
print(handles)

class TweetsSpider(scrapy.Spider):
    name = 'tweets'
    allowed_domains = ['twitter.com']
    start_urls = []
    for handle in handles:
        start_urls.append('http://twitter.com/' + handle)


    def parse(self, response):
        yield response.body.extract()
