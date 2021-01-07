# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    birthday = models.DateField(blank=True, null=True)


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    restaurant_type = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    open_hour = models.TimeField()
    close_hour = models.TimeField()

    def __str__(self):
        return self.name


class Product(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="product_restaurant")
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    photo = models.FileField(upload_to='products/', blank=True, null=True)
    price = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{} belongs to {} restaurant and has the price of {} ron".format(self.name, self.restaurant.name, self.price)


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restaurant")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField()
    payment_method = models.CharField(max_length=10)
    total_price = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{} did the order at the {} restaurant on {}".format(self.customer.name, self.restaurant.name, self.order_date)

