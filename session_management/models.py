from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Users(models.Model):
    user_id=models.AutoField(primary_key=True)
    user=models.CharField(max_length=18, unique=True)
    password=models.CharField(max_length=32)
    email=models.EmailField(unique=True, null=True)
    mobile = PhoneNumberField(unique=True, null=True)
    born_date=models.DateField()
    id_hash=models.CharField(max_length=15, unique=True)
    admin=models.BooleanField(default=False)