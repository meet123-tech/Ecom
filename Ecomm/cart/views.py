from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from  shop.models import Product
from django.http import JsonResponse 
from django.contrib import messages

# Create your views here.


def cart_summary(request):

    cart = Cart(request)
    products = cart.get_products
    quantities = cart.get_quants


    return render(request,'cart_summary.html',{'cart_products':products , 'prod_quantities':quantities})


def add_cart(request):

    cart = Cart(request)
    
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qunt = request.POST.get('product_qunt')
        # print(product_id)
        product = get_object_or_404(Product,id = product_id)

        cart.add(product=product,quantity=product_qunt)
        messages.success(request, f'{product.name} Added to Cart Successfully!...')
        cart_quantity = cart.__len__()

        response = JsonResponse({
           
           'qunt':cart_quantity
        })

        return response


    

def update_cart(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qunt = request.POST.get('product_qunt')

        cart.update(product=product_id,quantity=product_qunt)
        messages.success(request,'Cart Updated Successfuly')
        response = JsonResponse({'quantity':product_qunt})
        return response
        # return redirect('cart_summary')



def delete_cart(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        cart.delete(product=product_id)
        messages.success(request, 'item deleted Successfuly')
        response = JsonResponse({'product': product_id})
        return response
        # return redirect('cart_summary')
