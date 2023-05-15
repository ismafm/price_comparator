import json
import logging
import time
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
import scrapydo



class ebay_spider(scrapy.Spider):
    name = "peter_parker"

    product_list = []
    product_search = "cartera+hombre"

    start_urls = [
        "https://www.ebay.es/sch/i.html?_nkw=" + product_search
    ]



    def parse(self, response):
        urls = response.xpath("//li[contains(@id,'item')]//a[@class='s-item__link']/@href")[:25].getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_product_info)
    def extract_product_info(self,response):
        product = {}
        product["name"] = response.xpath("//h1[@class='x-item-title__mainTitle']//span/text()").get()
        product["price"] = response.xpath("//div[@class='x-bin-price__content']//span[contains(.,'EUR')]/text()").get()
        product["photo"] = response.xpath("//div[contains(@class,'active')]//img/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = response.xpath("//li[@class='ux-seller-section__item'][last()]//span[@class='ux-textspans']/text()").get()
        ebay_spider.product_list.append(product)
    @staticmethod
    def empty_product_list():
        ebay_spider.product_list = []
