from time import sleep

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor
from pathlib import Path
from recopilador_productos.recopilador_productos.items import product_info
from scrapy.utils.log import configure_logging
import scrapy


product_list = []
product_search = ""

class ebay_spider(scrapy.Spider):
    name = "peter_parker"

    start_urls = [
        "https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=" + "cartera+hombre" + "&_sacat=0"
    ]

    def parse(self, response):
        urls = response.xpath("//li[contains(@id,'item')]//a[@class='s-item__link']/@href")[:25].getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_product_info)

    def extract_product_info(self,response):
        product = product_info()
        global product_list
        product["name"] = response.xpath("//h1[@class='x-item-title__mainTitle']//span/text()").get()
        product["price"] = response.xpath("//span[@itemprop='price']/@content").get()
        product["photo"] = response.xpath("//div[contains(@class,'active')]//img/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = response.xpath("//li[@class='ux-seller-section__item'][last()]//span[@class='ux-textspans']/text()").get()
        product_list.append(product)



#Start the sctraping action
# def scrap_action(product):
#     #transfer the product search into the global var
#     global product_search
#     product_search = product
#     process = CrawlerProcess()
#     process.crawl(ebay_spider)
#     process.start()
ruta = "hola.txt"
f = open(ruta,'w')
f.write("¡¡puta!!")
f.close()