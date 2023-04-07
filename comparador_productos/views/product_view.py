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
    cheapest_products = [None, None, None, None]
    prueba = None
    #select the cheapest product in the list and put un cheapest_products list
    def slct_cheapest_one(product_price, product_name, product_photo):
        for position_price in range(len(product_price)):

            #select only the numeric part of the price
            price = product_price[position_price].text
            # replaces the commas with the period to make a numeric parse

            #range allout products and select cheapest ones
            for position_product in range(len(cheapest_products)):

                # select one product from the list
                product = cheapest_products[position_product]

                if product is None or float(product.getPrice().replace(",",".")) > float(price.replace(",",".")):

                    new_product = Products_repository(product_name[position_price].text,price, product_photo[position_price].get_attribute("src"))
                    cheapest_products[position_product] = new_product
                    break


    driver = webdriver.Firefox()
    #wait = WebDriverWait(driver, 10)
    #element = wait.until(EC.element_to_be_clickable((By.ID, 'someid')))
    driver.get("https://www.amazon.es/s?k=cactus+parlante")
#    time.sleep(10)
    name = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] div div div div div:nth-child(2) div[class*='s-title-instructions-style'] h2 a span")[0:40]
    img = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] div div div div div:nth-child(1) span a div img")[0:40]
    price = driver.find_elements(By.CSS_SELECTOR, "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] div div div div div:nth-child(2) div[class*='s-price-instructions-style'] div[class*='a-color-base'] a span span[aria-hidden='true'] span[class='a-price-whole']")[0:40]

    slct_cheapest_one(price,name,img)
    #driver.close()
    ##NO ENCUENTRA UN PRECIO BARATO
    return HttpResponse(name[17].text + " || "+ price[17].text + " || " + "<img src="+img[17].get_attribute("src")+">")#cheapest_products[0].getPrice())#price[6].text)
    #name[15].text + " || "+ price[15].text + " || " + "<img src="+img[15].get_attribute("src")+">"
    #return render(request, "prueba.html", {"tuplita":cheapest_products})
