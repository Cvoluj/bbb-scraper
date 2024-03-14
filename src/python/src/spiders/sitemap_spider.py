import scrapy
import logging
from scrapy.http import Response
from scrapy.selector import Selector
from items import UrlItem

from pipelines import UrlDatabasePipeline
from rmq.utils.import_full_name import get_import_full_name

class SitemapSpider(scrapy.Spider):
    name = 'sitemap'
    allowed_domains = ['bbb.org']

    proxy_enabled = True

    start_urls = ['https://www.bbb.org/sitemap-business-profiles-index.xml']

    custom_settings = {"ITEM_PIPELINES": {get_import_full_name(UrlDatabasePipeline): 310,}}

    def parse(self, response: Response):
        xml_content = response.body
        selector = Selector(text=xml_content)
        bussines_profile_page = selector.xpath("//sitemap/loc/text()").extract()

        for page in bussines_profile_page:
            yield scrapy.Request(page, callback=self.parse_sitemap)

    def parse_sitemap(self, response: Response):
        xml_content = response.body
        selector = Selector(text=xml_content)

        urls = selector.xpath('//url/loc/text()').getall()
        
        for url in urls:
            url_item = UrlItem(url=url)
            yield url_item
