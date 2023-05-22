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
    prueba = ""
    product_list = []
    product_search = "cartera-hombre"
    global_url = []

    def numeric_price_field(self, price):
        #select only the numeric part in price field
        if price is None:
            price = '999999999999999'
        real_price = price.replace("€","")
        real_price = real_price.replace(" ","")
        real_price = real_price.replace(",",".")
        return float(real_price)

    def numeric_rate_field(self, rate):
        #select only the numeric part in rate field and adapt to compare with others product rate
        if rate is None:
            rate = price = '999999999999999'
        real_rate = rate.replace(" ","")
        real_rate = real_rate.replace(",",".")
        real_rate = float(real_rate)*10
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
        driver.close()
    def parse(self, response):
        product = {}
        product["name"] = response.xpath("//span[@id='productTitle']/text()").get().strip()
        product["price"] = self.numeric_price_field(response.xpath("//div[@id='corePriceDisplay_desktop_feature_div']//span[@class='a-offscreen']/text()").get())
        product["photo"] = response.xpath("//img[@id='landingImage']/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = self.numeric_rate_field(response.xpath("//span[@class='a-declarative']//a[@role='button']//span[@class='a-size-base a-color-base']/text()").get())
        product["logo"] = "img/shop_logos/logo_amazon.png"
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



driver = webdriver.Firefox()
driver.get("https://www.amazon.es/s?k=cartera+hombre")
search_urls = driver.find_elements(By.XPATH, "//div[contains(@class,'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')]//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")[:30]
amazon_spider.global_url = search_urls
c = CrawlerProcess()
c.crawl(amazon_spider)
c.start()
print(amazon_spider.product_list)
print(len(amazon_spider.product_list))
print(len(search_urls))