from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from shop.models import Product
from django.dispatch import receiver
import datetime

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    shipping_full_name = models.CharField(max_length=100)
    shipping_email = models.EmailField(max_length=100)
    shipping_address1 = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100, null=True, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=50, null=True, blank=True)
    shipping_postal_code = models.CharField(max_length=20, null=True, blank=True)
    shipping_country = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()


post_save.connect(create_shipping, sender=User)


class Order(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    shipping_address = models.CharField(max_length=10000)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_status = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"Order - {str(self.id)}"
    
@receiver(pre_save, sender=Order)
def set_shipped_date_on_update(sender, instance, **kwargs):
    if instance.pk:
        current_time = datetime.datetime.now()
        obj = sender._default_manager.get(id=instance.pk)
        if instance.shipping_status and not obj.shipping_status:
            instance.date_shipped = current_time



        

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order Item - {str(self.id)}"