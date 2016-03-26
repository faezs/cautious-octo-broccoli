import string

from scraper_app.items import Listing
from scrapy import Spider, Request
from scrapy.contrib.loader.processor import Join, MapCompose
from scrapy.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector


class Canada411Spider(Spider):
    """Spider for names, numbers and addresses on Canada411.ca"""
    name = "Canada411"
    allowed_domains = "http://www.Canada411.ca/"
    start_urls = [allowed_domains + x for x in string.uppercase]
    listings_table_xpath = '//*[@id="c411Body"]/div[2]/div[1]/div[2]'
    item_fields = {
        'name': '//*[@id="contact"]/span[1]/h1',
        'number': '//*[@id="contact"]/span[2]',
        'address': '//*[@id="contact"]/span[3]',
        'locality': '//*[@id="contact"]/span[4]'
    }

    def url(self, other):
        return str(self.allowed_domains + other)

    def parse_items(self, response):
        selector = HtmlXPathSelector(response)
        print 'parsing page'
        for listing in selector.select(self.listings_table_xpath):
            loader = XPathItemLoader(Listing(), selector=listing)
            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()
            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
                yield loader.load_item()

    def parse_locations(self, response):
        for href in response.xpath('//*[@id="c411BrowserRightContent"]/div/div[1]/ul/li/h3/a/@href'):
            url = self.url(href.extract())
            print 'level4'
            yield Request(url, callback=self.parse_items)

    def parse_links2(self, response):
        for href in response.xpath('//*[@id="c411BrowserRightContent"]/div/ul/li/a/@href'):
            url = self.url(href.extract())
            print 'level3'
            yield Request(url, callback=self.parse_locations)

    def parse_links1(self, response):
        print response.xpath('//*[@id="c411BrowserRightContent"]/div/')
        for href in response.xpath('//*[@id="c411BrowserRightContent"]/div/ul/li/a/@href'):
            url = self.url(href.extract())
            print 'level2'
            yield Request(url, callback=self.parse_links2)

    def parse(self, response):
        for href in response.xpath('//*[@id="c411BrowserRightContent"]/div/ul/li/a/@href'):
            url = self.url(href.extract())
            print url
            yield Request(url, callback=self.parse_links1)
