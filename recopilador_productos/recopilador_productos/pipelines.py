# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
import json


class ScrapytutorialPipeline:
    def process_item(self, item, spider):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def open_spider(self, spider):
        self.file = open('products.json', 'w')

    def close_spider(self, spider):
        self.file.close()
