from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from scraper_app.items import IslamabadCafes


class ISnobSpider(BaseSpider):
    """Spider for cafe addresses on islamabadsnob.com"""
    name = "islamabadsnob"
    allowed_domains = "islamabadsnob.com"
    start_urls = ["http://www.islamabadsnob.com/cafes_coffee_shops_islamabad.htm"]
    cafes_table_xpath = '/html/body/table[2]/tbody/tr/td[3]/table/tbody/tr/td[1]/table/tbody/tr/td'
    item_fields = {
	'name' : '//*[@id="table649"]/tbody/tr/td/b[1]/font',
	'address' : '//*[@id="table637"]/tbody/tr/td[1]/font[2]',
    }

    def parse(self, response):
        selector = HtmlXPathSelector(response)


	# iterate over cafes
	for cafe in selector.select(self.cafes_table_xpath):
	    loader = XPathItemLoader(IslamabadCafes(), selector=cafe)

	    loader.default_input_processor = MapCompose(unicode.strip)
	    loader.default_output_processor = Join()

	    for field, xpath in self.item_fiels.iteritems():
		loader.add_xpath(field, xpath)
	    yield loader.load_item()


