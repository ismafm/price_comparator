import time

import scrapy
import scrapydo
import scrapydo
from scrapy.crawler import CrawlerProcess
import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

class pccom_spider(scrapy.Spider):
    name = "peter_parker"

    product_list = []
    product_search = "gtx%201660"

    def start_requests(self):
        headers = {
            'User-Agent': 'my-cool-project (+http://blogscuriosos.atwebpages.com/)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://pccomponentes.com/'
        }
        urls = [
            "https://www.pccomponentes.com/gigabyte-geforce-gtx-1660-super-d6-6gb-gddr6"
        ]
        for url in urls:
            yield scrapy.Request(url=url,headers=headers, callback=self.parse)

    def parse(self, response):
        pccom_spider.product_list = response.xpath("//h1/text()")
        # urls = response.xpath("//div[@id='product-grid']//a/@href")[0:30].getall()
        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.extract_product_info)

    def numeric_price_field(self, price):
        #select only the numeric part in price field
        if price is None:
            price = float("+inf")
        real_price = price.replace("Aproximadamente","")
        real_price = real_price.replace("EUR","")
        real_price = real_price.replace(" ","")
        real_price = real_price.replace("c/u","")
        real_price = real_price.replace(",",".")
        return float(real_price)

    def numeric_rate_field(self, rate):
        #select only the numeric part in rate field
        if rate is None:
            rate = float("-inf")
        real_rate = rate.replace(" ","")
        real_rate = real_rate.replace(",",".")
        real_rate = real_rate.replace("(","0")
        return float(real_rate.split("%")[0])

    def extract_product_info(self,response):
        product = {}
        product["name"] = response.xpath("//div[@class='ficha-producto__encabezado white-card-movil']//h1/text()").get()
        product["price"] = response.xpath("//div[@id='precio-main']/text()").get()
        product["photo"] = response.xpath("//img[@class='pc-com-zoom img-fluid']/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = response.xpath("//div[contains(@class,'valoracion')]//div[@class='percentage']/text()").get()
        product["logo"] = "img/shop_logos/logo_amazon.jpg"
        product["shop_link"] = "https://pccomponentes.com"
        pccom_spider.product_list.append(product)
    @staticmethod
    def empty_product_list():
        pccom_spider.product_list = []
    @staticmethod
    def empty_product_search():
        pccom_spider.product_search = ""
    @staticmethod
    def set_product_search(product_search):
        pccom_spider.product_search = product_search
# a = CrawlerProcess()
# a.crawl(pccom_spider)
# a.start()
#print(pccom_spider.product_list)
