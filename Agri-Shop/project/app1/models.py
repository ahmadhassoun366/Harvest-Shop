from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/product_images')

    def __str__(self):
        return f"Product {self.name} {self.unit_price} {self.farmer}"


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.client}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
