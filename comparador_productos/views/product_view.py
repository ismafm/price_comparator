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
from copy import deepcopy
from selenium.webdriver.support import expected_conditions as EC
import time

def shw_product(request):
    #first place for the cheapest product
    cheapest_products = [None, None, None, None, None, None, None, None, None, None]
    prueba = None
    #recompone la lista cuando hay un valor mas barato para llevarlo a una posicion mas baja.
    def prueba_tupla(number, product):
        list = [None, None, None, None, None, None, None, None, None, None]
        var = 0
        for l in range(len(list)):
            if l is number:
                list[l] = product
                var+=1
            else:
                list[l] = cheapest_products[l-var]

        return list
    #select the cheapest product in the list and put un cheapest_products list
    def slct_cheapest_one(product_price, product_name, product_photo,product_link):
        nonlocal cheapest_products
        for position_price in range(len(product_price)):

            #select only the numeric part of the price
            price = product_price[position_price].text
            # replaces the commas with the period to make a numeric parse

            #range allout products and select cheapest ones
            for position_product in range(len(cheapest_products)):

                # select one product from the list
                product = cheapest_products[position_product]

                if product is None or float(product.getPrice().replace(",",".")) > float(price.replace(",",".")):

                    new_product = Products_repository(product_name[position_price].text,price, product_photo[position_price].get_attribute("src"),product_link[position_price].get_attribute("href"))

                    cheapest_products = prueba_tupla(position_product, new_product)
                    break

    driver = webdriver.Firefox()
    #Busca los 25 primeros productos de amazon y los manda a comparar
    def search_amazon_products(driver):
        busqueda = "cartera hombre"
        busqueda.replace(" ","+")
        pagina = "https://www.amazon.es/s?k="+busqueda+"&rh=p_n_deal_type%3A26902953031"
        driver.get(pagina)

        name = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] span[class*='a-text-normal']")[0:25]
        img = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] span[data-component-type='s-product-image'] img[class='s-image']")[0:25]
        price = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] div[class*='s-price-instructions-style'] span[class='a-price']:first-child span[class='a-price-whole']")[0:25]
        link = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] span[data-component-type='s-product-image'] a")[0:25]

        slct_cheapest_one(price,name,img,link)
        driver.close()
    def search_ebay_products(driver):
        busqueda = "cartera hombre"
        busqueda.replace(" ", "+")
        pagina = "https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=cartera+hombre&_sacat=0"

        driver.get(pagina)

        name = driver.find_elements(By.CSS_SELECTOR, ".srp-results > .s-item__pl-on-bottom span[role='heading']")
        return HttpResponse(name[0].text)

    hi = search_ebay_products(driver)

    return HttpResponse(hi)
    #return render(request, "prueba.html", {"tuplita":cheapest_products})
