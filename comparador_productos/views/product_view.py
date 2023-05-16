import json

from django.shortcuts import render, redirect
from product_management.repositories.Products_repository import Products_repository
from django.http import HttpResponse
from django.shortcuts import render
import scrapydo
from recopilador_productos.recopilador_productos.spiders.ebay_spider import ebay_spider
from operator import itemgetter

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


    def sort_by_price(list):
        return sorted(list, key=itemgetter("price"))

    #Selecciona el tipo de ordenado que se haya pedido
    def sorting_type(list, sort_type):
        if sort_type == "Precio":
            return sort_by_price(list)
    def ebay_products(search_product, sort_type):
        scrapydo.setup()
        scrapydo.run_spider(ebay_spider)
        cheapest_products = sorting_type(ebay_spider.product_list, sort_type)
        ebay_spider.empty_product_list()
        return cheapest_products
    #product to search
    product_name = request.GET["product"].replace(" ", "+")
    # Obtain the sort type from the form
    sort_type = request.GET["sort_type"]
    # first place for the cheapest product
    list = ebay_products(product_name, sort_type)
    request.session["lists"] = [json.dumps(list),]
    return redirect("/result/")
    #return render(request, "result.html", {"tuplita": cheapest_products})



def shw_product(request):
    list = request.session["lists"][0]
    #return HttpResponse(list)
    return render(request, "result.html", {"tuplita": list})