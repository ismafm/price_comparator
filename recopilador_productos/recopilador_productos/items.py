# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field
import scrapy


class product_info(scrapy.Item):
    _name = Field()
    _price = Field()
    _photo = Field()
    _link = Field()

