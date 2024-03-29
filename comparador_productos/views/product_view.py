import json

from django.shortcuts import render, redirect
from product_management.repositories.Products_repository import Products_repository
from django.http import HttpResponse
from django.shortcuts import render
import scrapydo
from recopilador_productos.recopilador_productos.spiders.ebay_spider import ebay_spider
from recopilador_productos.recopilador_productos.spiders.amazon_spider import amazon_spider
from recopilador_productos.recopilador_productos.spiders.alibaba_spider import alibaba_spider
from operator import itemgetter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from session_management.repositories.Users_repository import Users_repository
from product_management.repositories.Products_repository import Products_repository
import json
#Pagina que se mostrará al entrar a la pagina a menos que se inicie sesión
def principal_page(request):
    if "usr_session" in request.session and request.session["usr_session"] != "":
        return redirect("/search/")
    return HttpResponse("<a href='/login/'><button>Login</button></a>")
#pagina de busqueda de productos. En ella solo se podran acceder los usuarios registrados
def search_page(request):
    if "usr_session" not in request.session or request.session["usr_session"] == "":
        return redirect("/")
    hash = Users_repository(id_hash=request.session["usr_session"])
    usr = hash.hash_user()
    return render(request, "search.html", {"profile_img":usr.profile_photo})

def calc_product(request):
    if "usr_session" not in request.session or request.session["usr_session"] == "":
        return redirect("/")
    def sort_list(list, dic_name, order):
        return sorted(list, key=itemgetter(dic_name), reverse=order)

    #Selecciona el tipo de ordenado que se haya pedido
    def sorting_type(list, sort_type):
        if sort_type == "price":
            return sort_list(list, "price", False)
        elif sort_type == "rate":
            return sort_list(list, "rate_seller", True)
    #remove the content in the class vars
    def purge_spider(spider):
        spider.empty_product_list()
        spider.empty_product_search()

    def ebay_products(search_product):
        ebay_spider.set_product_search(search_product)
        scrapydo.setup()
        scrapydo.run_spider(ebay_spider)
        cheapest_products = ebay_spider.product_list
        purge_spider(ebay_spider)
        return cheapest_products
    def amazon_products(search_product):

        driver = webdriver.Firefox()
        driver.get("https://www.amazon.es/s?k="+search_product)
        search_urls = driver.find_elements(By.XPATH, "//div[contains(@class,'sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20')]//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")[:30]
        # saves the urls obtained by selenium in the global_url amazon_spider class var
        amazon_spider.global_url = search_urls
        scrapydo.setup()
        scrapydo.run_spider(amazon_spider)
        list = amazon_spider.product_list
        driver.close()
        amazon_spider.restart_spider()
        return list
    def alibaba_products(search_product):
        driver = webdriver.Firefox()
        driver.get("https://spanish.alibaba.com/trade/search?assessmentCompany=true&keywords="+search_product+"&moqt=1")
        search_urls = driver.find_elements(By.XPATH, "//a[contains(@class,'search-card-e-slider__link')]")[:30]
        if len(search_urls) == 0:
            search_urls = driver.find_elements(By.XPATH, "//a[contains(@class,'elements-title-normal one-line')]")[:30]
        # saves the urls obtained by selenium in the global_url amazon_spider class var
        alibaba_spider.global_url = search_urls
        scrapydo.setup()
        scrapydo.run_spider(alibaba_spider)
        list = alibaba_spider.product_list
        driver.close()
        alibaba_spider.restart_spider()
        return list
    #product to search
    product_name = request.GET["product"].replace(" ", "+")
    # Obtain the sort type from the form
    sort_type = request.GET["sort_type"]
    #obtain ebay products only
    ebay_list = ebay_products(product_name)
    ebay_list = sorting_type(ebay_list, sort_type)[:10]
    #obtain amazon products only
    amazon_list = amazon_products(product_name)
    amazon_list = sorting_type(amazon_list, sort_type)[:10]
    alibaba_list = alibaba_products(product_name)
    alibaba_list = sorting_type(alibaba_list,sort_type)[:10]

    # General list of cheapest products
    general_list = sorting_type(alibaba_list+amazon_list+ebay_list,sort_type)[:10]
    request.session["lists"] = [general_list,amazon_list,ebay_list,alibaba_list]
    return redirect("/result/")
    #return render(request, "result.html", {"tuplita": cheapest_products})
def shw_product(request):
    if "usr_session" not in request.session or request.session["usr_session"] == "":
        return redirect("/")
    general_list = request.session["lists"][0]
    amazon_list = request.session["lists"][1]
    ebay_list = request.session["lists"][2]
    alibaba_list = request.session["lists"][3]

    hash = Users_repository(id_hash=request.session["usr_session"])
    usr = hash.hash_user()
    #return HttpResponse(list)
    return render(request, "result.html", {"general_list": general_list,"amazon_list": amazon_list,"ebay_list": ebay_list,"alibaba_list": alibaba_list,"profile_img":usr.profile_photo})
#Guarda el producto en la base de datos
def save_product(request):
    #product_id = None, name = None, price = None, photo = None, logo = None, link = None
    product = request.POST["product"].replace("\'","\"")
    json_product = json.loads(product)
    #Obtain the user id from the database
    usr_id = Users_repository(id_hash=request.session["usr_session"])
    usr_id = usr_id.hash_user().user_id
    #producto de la base de datos
    db_product = Products_repository(name=json_product["name"],price=float(json_product["price"]),photo=json_product["photo"],logo=json_product["logo"],link=json_product["link"],rate_seller=float(json_product["rate_seller"]),
                                     shop_link=json_product["shop_link"],fk_user_id=usr_id)
    db_product.new_product()
    return redirect("/result/")
