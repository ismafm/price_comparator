from product_management.models import Products
class Products_repository():
    def __init__(self,product_id=None,name=None,price=None,photo=None,logo=None,link=None, shop_link=None,rate_seller=None,fk_user_id=None):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._photo = photo
        self._logo = logo
        self._link = link
        self._shop_link = shop_link
        self._rate_seller = rate_seller
        self._fk_user_id = fk_user_id
    #saves the object in the database
    def new_product(self):
        product = Products(name=self._name,price=self._price,photo=self._photo,logo=self._logo,link=self._link,rate_seller=self._rate_seller,shop_link=self._shop_link,
                           fk_user_id=self._fk_user_id)
        product.save()
    #return products that the user likes
    def product_likes(self):
        products = Products.objects.all().filter(fk_user_id=self._fk_user_id)
        return products

    def getPrice(self):
        return self._price
    def setPrice(self,price):
        self._price = price
    def getName(self):
        return self._name
    def setName(self,name):
        self._name = name
    def getPhoto(self):
        return self._photo
    def setPhoto(self,photo):
        self._photo = photo
    def getLink(self):
        return self._link
    def setLink(self,link):
        self._link = link
