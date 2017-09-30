from django.contrib.auth.models import Permission, User
from django.db import models


class Boutique(models.Model):
    user = models.ForeignKey(User, default=1)
    shop_name= models.CharField(max_length=500)
   


    def __str__(self):
        return self.shop_name


class Product(models.Model):
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250)
    product_img = models.FileField()
    product_price = models.FloatField(max_length=100)
    product_desc = models.CharField(max_length=500)
     

    def __str__(self):
        return self.product_name
