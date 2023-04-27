from scrapy.crawler import CrawlerProcess
from pathlib import Path
from recopilador_productos.recopilador_productos.items import product_info
import scrapy
hi = ""
class ebay_spider(scrapy.Spider):
    name = "peter_parker"

    start_urls = [

        "https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=" + "cartera+hombre" + "&_sacat=0"

    ]
    def parse(self, response):
        global hi
        item = product_info()
        item["_name"] = response.xpath("//li[contains(@id,'item')]//div[contains(@class,'s-item__title')]//span/text()").get()
        hi = item
        return hi

#Start the sctraping action
def scrap_action():
    search_info = ""
    process =CrawlerProcess()
    process.crawl(ebay_spider)
    process.start()

scrap_action()
print(hi)