from django.db import models

# Create your models here.

class Products(models.Model):
    product_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000, unique=False)
    price=models.FloatField(null=True)
    price = models.FloatField(null=True)
    photo=models.CharField(max_length=1000, unique=False)
    logo=models.CharField(max_length=100, unique=False)
    link=models.CharField(max_length=3000, unique=False, default=None)
    shop_link=models.CharField(max_length=1000, unique=False, default=None)
    rate_seller=models.FloatField(default=None)
    fk_user_id=models.IntegerField(default=0)
