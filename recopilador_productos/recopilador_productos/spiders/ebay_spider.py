import time

import scrapy
import scrapydo
import scrapydo
from scrapy.crawler import CrawlerProcess


class ebay_spider(scrapy.Spider):
    name = "peter_parker"

    product_list = []
    product_search = "cartera+hombre"
    contador = 0

    start_urls = [
        "https://www.ebay.es/sch/i.html?_nkw=" + product_search
    ]
    def parse(self, response):
        urls = response.xpath("//li[contains(@id,'item')]//a[@class='s-item__link']/@href")[0:30].getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_product_info)

    def numeric_price_field(self, price):
        #select only the numeric part in price field
        if price is None:
            price = "999999999"
        real_price = price.replace("Aproximadamente","")
        real_price = real_price.replace("EUR","")
        real_price = real_price.replace(" ","")
        real_price = real_price.replace("c/u","")
        real_price = real_price.replace(",",".")
        return float(real_price)

    def numeric_rate_field(self, rate):
        #select only the numeric part in rate field
        if rate is None:
            price = "999999999"
        real_rate = rate.replace(" ","")
        real_rate = real_rate.replace(",",".")
        real_rate = real_rate.replace("(","0")
        return float(real_rate.split("%")[0])

    def extract_product_info(self,response):
        product = {}
        product["name"] = response.xpath("//h1[@class='x-item-title__mainTitle']//span/text()").get()
        product["price"] = self.numeric_price_field(response.xpath("//div[@class='x-bin-price__content']//span[contains(.,'EUR')]/text()").get())
        product["photo"] = response.xpath("//div[contains(@class,'active')]//img/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = self.numeric_rate_field(response.xpath("//li[@class='ux-seller-section__item'][last()]//span[@class='ux-textspans']/text()").get())
        product["logo"] = "img/shop_logos/logo_ebay.jpg"
        ebay_spider.contador+=1
        ebay_spider.product_list.append(product)
    @staticmethod
    def empty_product_list():
        ebay_spider.product_list = []


# a = CrawlerProcess()
# a.crawl(ebay_spider)
# a.start()
