from django.shortcuts import render,get_object_or_404
from .cart import Cart
from  shop.models import Product
from django.http import JsonResponse 

# Create your views here.


def cart_summary(request):

    cart = Cart(request)
    products = cart.get_products


    return render(request,'cart_summary.html',{'cart_products':products})


def add_cart(request):

    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        print(product_id)
        product = get_object_or_404(Product,id = product_id)

        cart.add(product=product)

        cart_quantity = cart.__len__()

        response = JsonResponse({
           
           'qunt':cart_quantity
        })

        return response


    pass

def update_cart(request):
    pass


def delete_cart(request):
    pass
