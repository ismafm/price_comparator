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
    # recompone la lista cuando hay un valor mas barato para llevarlo a una posicion mas baja.
    def add_new_cheapest(number, product):
        list = [None, None, None, None, None, None, None, None, None, None]
        var = 0
        for l in range(len(list)):
            if l is number:
                list[l] = product
                var += 1
            else:
                list[l] = cheapest_products[l - var]

        return list

    # select the cheapest product in the list and put un cheapest_products list
    def slct_cheapest_one(product_price, product_name, product_photo, product_link):
        nonlocal cheapest_products
        # range allout products and select cheapest ones
        for position_price in range(len(product_price)):

            # select only the numeric part of the price
            price = product_price[position_price]#.text
            # replaces the commas with the period to make a numeric parse

            # range allout the cheapest product array and insert the compared product if is cheap
            for position_product in range(len(cheapest_products)):

                # select one product from the list
                product = cheapest_products[position_product]

                if product is None or float(product.getPrice().replace(",", ".")) > float(price.replace(",", ".")):
                    new_product = Products_repository(product_name[position_price].text, price,
                                                      product_photo[position_price].get_attribute("src"),
                                                      product_link[position_price].get_attribute("href"))

                    cheapest_products = add_new_cheapest(position_product, new_product)
                    break

    def numeric_price_field(price):
        #select only the numeric part in price field
        for i,j in enumerate(price):

            price[i] = j.text.split(' ')[0]

        return price

    # Busca los 25 primeros productos de amazon y los manda a comparar
    def search_amazon_products(driver, busqueda):
        busqueda.replace(" ", "+")
        pagina = "https://www.amazon.es/s?k=" + busqueda + "&rh=p_n_deal_type%3A26902953031"
        driver.get(pagina)
        driver.refresh()

        name = driver.find_elements(By.CSS_SELECTOR,
                                    "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] span[class*='a-text-normal']")[
               0:25]
        img = driver.find_elements(By.CSS_SELECTOR,
                                   "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] span[data-component-type='s-product-image'] img[class='s-image']")[
              0:25]
        price = driver.find_elements(By.CSS_SELECTOR,
                                     "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] div[class*='s-price-instructions-style'] span[class='a-price']:first-child span[class='a-price-whole']")[
                0:25]
        link = driver.find_elements(By.CSS_SELECTOR,
                                    "div[data-asin^='B'][class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20'] span[data-component-type='s-product-image'] a")[
               0:25]

        price = numeric_price_field(price)
        slct_cheapest_one(price, name, img, link)
        #driver.close()

    def search_ebay_products(driver, busqueda):
        busqueda.replace(" ", "+")
        pagina = "https://www.ebay.es/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=" + busqueda + "&_sacat=0"

        driver.get(pagina)

        name = driver.find_elements(By.CSS_SELECTOR, ".srp-results > .s-item__pl-on-bottom span[role='heading']")[0:25]
        img = driver.find_elements(By.CSS_SELECTOR, ".srp-results > .s-item__pl-on-bottom .s-item__image img")[0:25]
        price = driver.find_elements(By.CSS_SELECTOR, ".srp-results > .s-item__pl-on-bottom .s-item__price")[0:25]
        link = driver.find_elements(By.CSS_SELECTOR, ".srp-results > .s-item__pl-on-bottom .s-item__link")[0:25]

        price = numeric_price_field(price)
        slct_cheapest_one(price, name, img, link)
    def search_aliexpress_products(driver, busqueda):
        busqueda.replace(" ", "+")
        pagina = "https://es.aliexpress.com/w/wholesale-cartera-hombre.html?SearchText=" + busqueda
        driver.get(pagina)
        link = driver.find_elements(By.CSS_SELECTOR, ".list--gallery--34TropR .manhattan--container--1lP57Ag")
        #refresh the pae until it shows it correctly
        while len(link)==0:
            driver.refresh()
            time.sleep(1)
            link = driver.find_elements(By.CSS_SELECTOR, ".list--gallery--34TropR .manhattan--container--1lP57Ag")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,1000)")
        time.sleep(1)
        driver.execute_script("window.scrollTo(1000,2000)")
        time.sleep(1)
        name = driver.find_elements(By.CSS_SELECTOR, ".list--gallery--34TropR .manhattan--container--1lP57Ag .manhattan--titleText--WccSjUS")[0:25]
        img = driver.find_elements(By.CSS_SELECTOR, ".list--gallery--34TropR .manhattan--container--1lP57Ag .product-img")[0:25]
        price = driver.find_elements(By.CSS_SELECTOR, ".list--gallery--34TropR .manhattan--container--1lP57Ag .manhattan--price-sale--1CCSZfK span:nth-child(n+2)")[0:75]
        link = driver.find_elements(By.CSS_SELECTOR, ".list--gallery--34TropR .manhattan--container--1lP57Ag")[0:25]

        correct_price = []
        real_position = 0
        for i in range(0,len(price),3):

            #verifica si hay un punto en la siguiente posicion. si no lo hay es que el numero no es decimal
            if price[i+1+real_position].text is not ".":
                correct_price.append(str(price[i + real_position].text))
                real_position -= 2
            else:
                correct_price.append(str(price[i+real_position].text)+str(price[i+1+real_position].text)+str(price[i+2+real_position].text))

        price = correct_price

        #price = correct_price

        slct_cheapest_one(price, name, img, link)

        #return "<a href='"+str(link[24].get_attribute("href"))+"'>"+str(name[24].text) + "</a>: Precio: " + str(price[24]) + "<img src='"+str(img[24].get_attribute("src"))+"'>"
        driver.close()


    product_name = request.GET["product"]
    # first place for the cheapest product
    cheapest_products = [None, None, None, None, None, None, None, None, None, None]
    driver = webdriver.Firefox()
    search_amazon_products(driver, product_name)
    search_ebay_products(driver, product_name)
    #search_aliexpress_products(driver, product_name)
    return render(request, "prueba.html", {"tuplita": cheapest_products})
    #return HttpResponse(hi)