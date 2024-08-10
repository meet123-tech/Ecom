from django.shortcuts import render
from .models import Product
# Create your views here.


def home(request):
    Products = Product.objects.all()
    return render(request,'home.html',{'products':Products})