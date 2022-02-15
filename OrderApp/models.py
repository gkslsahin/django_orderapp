from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    email_adress = models.EmailField(max_length=300)


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=250)


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=250)


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    restaurant =models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order_status = models.BooleanField(default=0)
