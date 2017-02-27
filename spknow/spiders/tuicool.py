# -*- coding: utf-8 -*-
import scrapy
from spknow import items

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36")
}


class TuicoolSpider(scrapy.Spider):
    name = "tuicool"
    allowed_domains = ["tuicool.com"]

    def start_requests(self):
        urls = [
            'http://www.tuicool.com/topics/11130000'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=HEADERS, callback=self.parse)

    def parse(self, response):
        urls = response.css('a.article-list-title::attr(href)').extract()
        for href in urls[:1]:
            yield scrapy.Request(response.urljoin(href),
                                 headers=HEADERS,
                                 callback=self.parse_article)

    def parse_article(self, response):
        article = items.Article(response.body.decode(), response.request.url)
        item = items.ArticleItem()
        item["title"] = article.title
        item["content"] = article.content
        yield item
