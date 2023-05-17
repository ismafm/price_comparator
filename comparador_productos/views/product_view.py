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
    def sort_list(list, dic_name, order):
        return sorted(list, key=itemgetter(dic_name), reverse=order)

    #Selecciona el tipo de ordenado que se haya pedido
    def sorting_type(list, sort_type):
        if sort_type == "price":
            return sort_list(list, "price", False)
        elif sort_type == "rate":
            return sort_list(list, "rate_seller", True)

    def ebay_products(search_product, sort_type):
        scrapydo.setup()
        scrapydo.run_spider(ebay_spider)
        cheapest_products = sorting_type(ebay_spider.product_list, sort_type)
        ebay_spider.empty_product_list()
        return cheapest_products[:10]
    #product to search
    product_name = request.GET["product"].replace(" ", "+")
    # Obtain the sort type from the form
    sort_type = request.GET["sort_type"]
    # first place for the cheapest product
    list = ebay_products(product_name, sort_type)
    request.session["lists"] = [list,]
    #return HttpResponse(str(ebay_spider.contador) + "  " + str(len(list)))
    return redirect("/result/")
    #return render(request, "result.html", {"tuplita": cheapest_products})



def shw_product(request):
    list = request.session["lists"][0]
    #return HttpResponse(list)
    return render(request, "result.html", {"tuplita": list})