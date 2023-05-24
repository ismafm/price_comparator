import time

import scrapy
import scrapydo
import scrapydo
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from lxml import etree
import requests
import random


class amazon_spider(scrapy.Spider):
    name = "miles_morales"
    product_list = []
    global_url = []

    def numeric_price_field(self, price):
        #select only the numeric part in price field
        if price is None:
            real_price = "inf"
        else:
            real_price = price.replace("€","")
            real_price = real_price.replace(" ","")
            real_price = real_price.replace(",",".")
        return float(real_price)

    def numeric_rate_field(self, rate):
        #select only the numeric part in rate field and adapt to compare with others product rate
        if rate is None:
            rate = '0'
        real_rate = rate.replace(" ","")
        real_rate = real_rate.replace(",",".")
        real_rate = int(float(real_rate)*20)
        return real_rate
    def start_requests(self):
        def random_number():
            return random.randrange(0,5)
        random_headers = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
                          "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"]
        headers = {
            'User-Agent': random_headers[random_number()],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.aliexpress.com/'
        }
        urls = amazon_spider.global_url
        for url in urls:
            yield scrapy.Request(url=url.get_attribute("href"),headers=headers, callback=self.parse)
    def parse(self, response):
        product = {}
        product["name"] = response.xpath("//span[@id='productTitle']/text()").get().strip()
        product["price"] = response.xpath("//div[@id='corePriceDisplay_desktop_feature_div']//span[@class='a-offscreen']/text()").get()
        #Obtiene una nueva busqueda en el caso de que el precio este en otro lugar
        if product["price"] is None:
            product["price"] = self.numeric_price_field(response.xpath("//div[@id='apex_desktop']//span[@aria-hidden='true']/text()").get())
        else:
            product["price"] = self.numeric_price_field(product["price"])
        product["photo"] = response.xpath("//img[@id='landingImage']/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = self.numeric_rate_field(response.xpath("//span[@class='a-declarative']//a[@role='button']//span[@class='a-size-base a-color-base']/text()").get())
        product["logo"] = "img/shop_logos/logo_amazon.png"
        product["shop_link"] = "https://www.amazon.es"
        amazon_spider.product_list.append(product)
    #get empty the spider´s info var
    @staticmethod
    def restart_spider():
        amazon_spider.product_list = []
        amazon_spider.global_url = []
    @staticmethod
    def empty_product_search():
        amazon_spider.product_search = ""



# driver = webdriver.Firefox()
# driver.get("https://www.amazon.es/s?k=camisa+hombre")
# search_urls = driver.find_elements(By.XPATH, "//div[contains(@class,'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')]//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")[:30]
# # saves the urls obtained by selenium in the global_url amazon_spider class var
# amazon_spider.global_url = search_urls
# c = CrawlerProcess()
# c.crawl(amazon_spider)
# c.start()
# print(amazon_spider.product_list)
# print(len(amazon_spider.product_list))
# print(len(search_urls))