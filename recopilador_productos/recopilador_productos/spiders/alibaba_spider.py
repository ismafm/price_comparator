import time

import scrapy
import scrapydo
import scrapydo
from scrapy.crawler import CrawlerProcess
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class alibaba_spider(scrapy.Spider):
    name = "Benjamin_Reilly"

    product_list = []
    product_search = "cartera+hombre"
    global_url = []

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
            'Referer': 'https://spanish.alibaba.com/'
        }
        urls = alibaba_spider.global_url

        for url in urls:
            yield scrapy.Request(url=url.get_attribute("href"),headers=headers, callback=self.parse)
    def numeric_price_field(self, price):
        #select only the numeric part in price field
        if price is None:
            real_price = float("+inf")
        else:
            real_price = price.split()[0]
            real_price = real_price.replace(",",".")
        return float(real_price)

    def numeric_rate_field(self, rate):
        #select only the numeric part in rate field
        if rate is None:
            real_rate = float("-inf")
        else:
            real_rate = rate.split("/")[0]
        return float(real_rate)*20
    def parse(self, response):
        product = {}
        product["name"] = response.xpath("//div[@class='product-title']//h1/text()").get()
        #busca el elemento en las posibles clases que lo puedan tener
        product["price"] = response.xpath("//div[@class='price']//span[@class='promotion']/text()").get()
        if product["price"] is None:
            product["price"] = response.xpath("//span[@class='price']/text()").get()
        elif product["price"] is None:
            product["price"] = response.xpath("//div[@class='promotion-price']//strong/text()").get()
        product["price"] = self.numeric_price_field(product["price"])

        product["photo"] = None
        product["video"] = response.xpath("//div[@class='bc-video-player']//video/@src").get()
        product["link"] = response.request.url
        product["rate_seller"] = self.numeric_rate_field(response.xpath("//div[@class='attr-content'][1]/text()").get())
        product["logo"] = "img/shop_logos/logo_alibaba.png"
        product["shop_link"] = "https://spanish.alibaba.com/"
        alibaba_spider.product_list.append(product)
        # get empty the spider´s info var
    @staticmethod
    def restart_spider():
        alibaba_spider.product_list = []
        alibaba_spider.global_url = []
    @staticmethod
    def set_product_search(product_search):
        alibaba_spider.product_search = product_search

# driver = webdriver.Firefox()
# driver.get("https://spanish.alibaba.com/trade/search?assessmentCompany=true&keywords=cartera+hombre&moqt=1")
# search_urls = driver.find_elements(By.XPATH, "//a[@class='elements-title-normal one-line']")[:30]
# # saves the urls obtained by selenium in the global_url amazon_spider class var
# alibaba_spider.global_url = search_urls
# a = CrawlerProcess()
# a.crawl(alibaba_spider)
# a.start()
# print(len(alibaba_spider.product_list))
