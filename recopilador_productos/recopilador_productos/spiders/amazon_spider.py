import time

import scrapy
import scrapydo
import scrapydo
from scrapy.crawler import CrawlerProcess


class amazon_spider(scrapy.Spider):
    name = "miles_morales"

    product_list = []
    product_search = "cartera+hombre"

    def start_requests(self):
        urls = [
            "https://www.amazon.es/s?k=" + amazon_spider.product_search
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath("//span[@data-component-type='s-search-results']//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href")[0:30].getall()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.extract_product_info)

    def numeric_price_field(self, price):
        #select only the numeric part in price field
        if price is None:
            price = float("+inf")
        real_price = price.replace("Aproximadamente","")
        real_price = real_price.replace("€","")
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
        product["name"] = response.xpath("//span[@id='productTitle']/text()").get()
        product["price"] = self.numeric_price_field(response.xpath("//div[@id='corePriceDisplay_desktop_feature_div']//span[@class='a-offscreen']/text()").get())
        product["photo"] = response.xpath("//img[@id='landingImage']/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = self.numeric_rate_field(response.xpath("//span[@id='acrPopover']//span[@class='a-size-base a-color-base']/text()").get())
        product["logo"] = "img/shop_logos/logo_amazon.jpg"
        product["shop_link"] = "https://www.amazon.es"
        amazon_spider.product_list.append(product)
    @staticmethod
    def empty_product_list():
        amazon_spider.product_list = []
    @staticmethod
    def empty_product_search():
        amazon_spider.product_search = ""
    @staticmethod
    def set_product_search(product_search):
        amazon_spider.product_search = product_search


a = CrawlerProcess()
a.crawl(amazon_spider)
a.start()
