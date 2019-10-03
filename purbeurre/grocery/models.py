#pylint: disable=C0103
""" Database created in python that define products and user favorites"""
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """ Categories defined with name"""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    """ Products defined with informations based on OpenFoodFacts database"""
    name = models.CharField(max_length=200)
    nutrigrade = models.CharField(max_length=1)
    image = models.URLField()
    url = models.URLField()
    nutrient = models.URLField(default='image')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default="")

    def __str__(self):
        return self.name

class Favorite(models.Model):
    """ Favorites defined with User and product as foreign keys"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
