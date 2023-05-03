from django.http import HttpResponse
from selenium.webdriver.support.wait import WebDriverWait

from session_management.repositories.Users_repository import Users_repository
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from product_management.repositories.Products_repository import Products_repository
from recopilador_productos.recopilador_productos.spiders.ebay_spider import ebay_spider
import recopilador_productos.recopilador_productos.spiders.ebay_spider
from scrapy.crawler import CrawlerProcess
from copy import deepcopy
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import signal
#____________________________________
from django.shortcuts import render
from django.http import HttpResponse
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from recopilador_productos.recopilador_productos.spiders import ebay_spider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer, task
import json


#Pagina que se mostrará al entrar a la pagina a menos que se inicie sesión
def principal_page(request):
    if request.session["usr_name"] != "":
        return redirect("/search/")
    return HttpResponse("<a href='/login/'><button>Login</button></a>")
#pagina de busqueda de productos. En ella solo se podran acceder los usuarios registrados
def search_page(request):
    if "usr_name" not in request.session or request.session["usr_name"] is "":
        return redirect("/")
    return render(request, "search.html")

def shw_product(request):
    def calling_spider():
        configure_logging()
        settings = get_project_settings()
        runner = CrawlerRunner(settings)

        def handle_error(failure):
            print(failure.getTraceback())
            reactor.stop()

        def stop_r():
            reactor.stop()

        def prueba():
            reactor.stop()
            yield runner.crawl(ebay_spider.ebay_spider).addCallback(stop_r()).addErrback(handle_error)

        prueba()
    # recompone la lista cuando hay un valor mas barato para llevarlo a una posicion mas baja.
    def add_new_cheapest(number, product, old_list):
        list = [None, None, None, None, None, None, None, None, None, None]
        var = 0
        for l in range(len(list)):
            if l is number:
                list[l] = product
                var += 1
            else:
                list[l] = old_list[l - var]

        return list

    # select the cheapest product in the list and put un cheapest_products list
    def slct_cheapest_one(product_list,cheapest_products_list):
        # range allout products and select cheapest ones
        for index, in_product in enumerate(product_list):

            # select only the numeric part of the price
            price = in_product["price"]
            # replaces the commas with the period to make a numeric parse

            # range allout the cheapest product array and insert the compared product if is cheap
            for position_product in range(len(cheapest_products_list)):

                # select one product from the list
                product = cheapest_products_list[position_product]

                if product is None or float(product.getPrice().replace(",", ".")) > float(price.replace(",", ".")):
                    new_product = Products_repository(in_product["name"], price,
                                                      in_product["photo"],
                                                      in_product["link"])

                    cheapest_products_list = add_new_cheapest(position_product, new_product, cheapest_products_list)
                    break

        return cheapest_products_list

    def numeric_price_field(price):
        #select only the numeric part in price field
        for i,j in enumerate(price):
            price[i] = j.text.split(' ')[0]
            price[i] = price[i].translate({ord("€"):None})
        return price

    def ebay_products(search_product,cheapest_products, product):
        calling_spider()
        f = open("comparador_productos/static/json/products.json")
        product_list = json.load(f)
        return product_list


    #product to search

    product_name = request.GET["product"].replace(" ", "+")




    # first place for the cheapest product
    cheapest_products = [None, None, None, None, None, None, None, None, None, None]
    cheapest_products = ebay_products(product_name,cheapest_products, product_name)
    #return render(request, "result.html",{"tuplita":cheapest_products})
    return HttpResponse(cheapest_products[0]["name"])