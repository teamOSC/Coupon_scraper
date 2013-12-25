#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spider 		import BaseSpider
from scrapy.selector 		import HtmlXPathSelector
from scrapy.http		import Request
import w3lib
from scrapy.cmdline import execute

class MySpider(BaseSpider):
	name 		= "nettuts"
	allowed_domains	= ["net.tutsplus.com"]
	start_urls	= ["http://net.tutsplus.com/"]

	def parse(self, response):
		hxs 	= HtmlXPathSelector(response)
		titles 	= hxs.select('//h1[@class="post_title"]/a/text()').extract()
		for title in titles:
			item = NettutsItem()
			item["title"] = title
			print item
			yield item

if __name__ == '__main__':
	execute(['scrapy crawl nettuts'])