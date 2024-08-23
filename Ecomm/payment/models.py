from django.db import models
from django.contrib.auth.models import User
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