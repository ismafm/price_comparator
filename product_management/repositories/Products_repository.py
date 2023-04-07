class Products_repository():

    def __init__(self,name=None,price=None,photo=None):
        self._name = name
        self._price = price
        self._photo = photo


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
