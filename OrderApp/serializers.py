from rest_framework import serializers
from OrderApp.models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ("user_id", "user_name", "surname", "email_adress")


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("restaurant_id", "restaurant_name")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("category_id", "category_name")


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ("food_id", "food_name", "category")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("order_id", "user", "food", "order_status")
