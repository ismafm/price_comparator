from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Rule, Request
from scrapy.linkextractors import LinkExtractor
from pathlib import Path
from recopilador_productos.recopilador_productos.items import product_info
from scrapy.utils.log import configure_logging
import scrapy

product_list = []
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
def scrap_action():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(ebay_spider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    return product_list
    