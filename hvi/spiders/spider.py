import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import HviItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class HviSpider(scrapy.Spider):
	name = 'hvi'
	start_urls = ['https://hvidbjergbank.dk/om-banken/nyheder/']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date"]/text()').get().strip()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="elementor-element elementor-element-16b7ee1 elementor-widget elementor-widget-theme-post-content"]/div[@class="elementor-widget-container"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=HviItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
