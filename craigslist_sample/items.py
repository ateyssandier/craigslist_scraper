# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CraigslistSampleItem(Item):
    # define the fields for your item here like:
    # name = Field()
    date = Field()
    bedrooms = Field()
    title = Field()
    link = Field()
    price = Field()
    location = Field()
    
    