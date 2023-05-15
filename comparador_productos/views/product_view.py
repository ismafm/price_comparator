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

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer, task
import json
import time
import threading
from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from django.shortcuts import render
import scrapydo
from recopilador_productos.recopilador_productos.spiders.ebay_spider import ebay_spider
import re


#Pagina que se mostrará al entrar a la pagina a menos que se inicie sesión
def principal_page(request):
    if "usr_name" in request.session and request.session["usr_name"] != "":
        return redirect("/search/")
    return HttpResponse("<a href='/login/'><button>Login</button></a>")
#pagina de busqueda de productos. En ella solo se podran acceder los usuarios registrados
def search_page(request):
    if "usr_name" not in request.session or request.session["usr_name"] is "":
        return redirect("/")
    return render(request, "search.html")

def calc_product(request):

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

    def numeric_price_field(price):
        #select only the numeric part in price field
        if price is None:
            price = "999999999"
        real_price = price.replace("Aproximadamente","")
        real_price = real_price.replace("EUR","")
        real_price = real_price.replace(" ","")
        real_price = real_price.replace("c/u","")
        return real_price


    # select the cheapest product in the list and put un cheapest_products list
    def slct_cheapest_one(product_list,cheapest_products_list):
        # range allout products and select cheapest ones
        for index, in_product in enumerate(product_list):

            # select only the numeric part of the price
            price = in_product["price"]
            price = numeric_price_field(price)
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



    def ebay_products(search_product,cheapest_products, product):
        scrapydo.setup()
        scrapydo.run_spider(ebay_spider)
        cheapest_products = slct_cheapest_one(ebay_spider.product_list, cheapest_products)
        ebay_spider.empty_product_list()
        return cheapest_products
    #product to search
    product_name = request.GET["product"].replace(" ", "+")

    # first place for the cheapest product
    cheapest_products = [None, None, None, None, None, None, None, None, None, None]
    cheapest_products = ebay_products(product_name,cheapest_products, product_name)
    #cheapest_products = ebay_spider().product_list
    return render(request, "result.html", {"tuplita": cheapest_products})
    #return redirect("/result/",cheapest_products)
    #return HttpResponse(str(re.search(r'\b\d+(?:[,.]\d+)?\b', cheapest_products[0]["price"]).group()) + " se supone que es lo mismo que " + str(cheapest_products[0]["price"]))
    #return HttpResponse(re.findall(r'\d+(?:[,.]\d+)?', cheapest_products[0]["price"]))

    #ebay_spider.empty_product_list()
    return HttpResponse(len(ebay_spider.product_list))

def shw_product(request):
    return render(request, "result.html", {"tuplita": list})