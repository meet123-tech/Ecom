from django.db import models
# from django.contrib.auth.models import User
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    # slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
    



class Customer(models.Model):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100,unique=True)
    password = models.CharField(max_length=128)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    



class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    description = models.TextField(max_length=250,blank=True,null=True,default='')
    image = models.ImageField(upload_to='upload/products/')

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    # stock = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=255,default="",blank=True)
    phone = models.CharField(max_length=50,default="",blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
