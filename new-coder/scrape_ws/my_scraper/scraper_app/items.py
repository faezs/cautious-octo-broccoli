from scrapy.item import Item, Field

class IslamabadCafes(Item):
    """Address container (Dictionary-like object) for scraped data"""
    title = Field()
    address = Field()
    
	
