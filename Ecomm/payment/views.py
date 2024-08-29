from django.shortcuts import render,redirect
from cart.cart import Cart
from .models import ShippingAddress
from .forms import ShippingForm,PaymentForm
from django.contrib import messages

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


def billing_info(request):

    if request.POST:

        cart = Cart(request) 
        products = cart.get_products
        quantities = cart.get_quants
        total = cart.cart_total


        if request.user.is_authenticated:
            billing_form = PaymentForm()
            my_shipping = request.POST
            request.session['shipping'] = my_shipping

            return render(request,  'payment/billing_info.html', {'cart_products': products , 'prod_quantities':quantities, 'totals':total, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request,  'payment/billing_info.html', {'cart_products': products, 'prod_quantities': quantities, 'totals': total, 'shipping_info': request.POST, 'billing_form': billing_form})

        # shipping_form = request.POST
        # return render(request,  'payment/billing_info.html', {'cart_products': products, 'prod_quantities': quantities, 'totals': total, 'shipping_form': shipping_form})
    else:
        messages.success(request,('Access Denied'))
        return redirect('home')
    

def process_order(request):
    
    if request.POST:

        billing_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('shipping') 
        print(my_shipping)
        messages.success(request,('Order Placed'))
        return redirect('home')

    else:
        messages.success(request,('Access Denied'))
        return redirect('home')
