from django.shortcuts import render
from cart.cart import Cart
from .models import ShippingAddress
from .forms import ShippingForm

# Create your views here.

def payment_success(request):
    return render(request, 'payment/payment_success.html',{})




def checkout(request):

    cart = Cart(request)
    products = cart.get_products
    quantities = cart.get_quants
    total = cart.cart_total

    

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(
            request.POST or None, instance=shipping_user)
        return render(request,  'payment/checkout.html', {'cart_products': products , 'prod_quantities':quantities, 'totals':total, 'shipping_form':shipping_form })
    else:
        shipping_form = ShippingForm(
            request.POST or None)
        return render(request,  'payment/checkout.html', {'cart_products': products , 'prod_quantities':quantities, 'totals':total, 'shipping_form':shipping_form })
