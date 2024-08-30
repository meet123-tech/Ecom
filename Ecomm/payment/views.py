from django.shortcuts import render,redirect
from cart.cart import Cart
from .models import ShippingAddress,Order,OrderItem
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
        total = cart.cart_total()


        if request.user.is_authenticated:
            billing_form = PaymentForm()
            my_shipping = request.POST
            request.session['shipping'] = my_shipping
            

            return render(request,  'payment/billing_info.html', {'cart_products': products , 'prod_quantities':quantities, 'totals':total, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            my_shipping = request.POST
            request.session['shipping'] = my_shipping
            return render(request,  'payment/billing_info.html', {'cart_products': products, 'prod_quantities': quantities, 'totals': total, 'shipping_info': request.POST, 'billing_form': billing_form})

        # shipping_form = request.POST
        # return render(request,  'payment/billing_info.html', {'cart_products': products, 'prod_quantities': quantities, 'totals': total, 'shipping_form': shipping_form})
    else:
        messages.success(request,('Access Denied'))
        return redirect('home')
    

def process_order(request):
    
    if request.POST:

        cart = Cart(request)
        products = cart.get_products
        quantities = cart.get_quants
        total = cart.cart_total()

        billing_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('shipping') 
        # print(f" asdsfasfesfeddsfasf ---------{my_shipping}")

        user = request.user
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}, {my_shipping['shipping_address2']}, {my_shipping['shipping_city']}, {my_shipping['shipping_state']}, {my_shipping['shipping_postal_code']}, {my_shipping['shipping_country']}"
        full_name = my_shipping['shipping_full_name']
        paid_amount = total 

        if user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address= shipping_address, paid_amount=paid_amount)
            create_order.save()

            order_id = create_order.pk

            for product in products():

                product_id = product.id

                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price

                for key, value in quantities().items():
                    if int(key) == product_id:
                        create_order_item = OrderItem.objects.create(order_id=order_id, product_id=product_id,user=user,
                                                 quantity=value, price=product_price)
                        create_order_item.save()
                        # messages.success(request, ('Product Added'))
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            messages.success(request, ('Order Placed'))
            return redirect('home')
        else:
            create_order = Order( full_name=full_name, email=email,
                                 shipping_address=shipping_address, paid_amount=paid_amount)
            create_order.save()

            order_id = create_order.pk

            for product in products():

                product_id = product.id

                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price

                for key, value in quantities().items():
                    if int(key) == product_id:
                        create_order_item = OrderItem.objects.create(order_id=order_id, product_id=product_id,
                                                                     quantity=value, price=product_price)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            messages.success(request, ('Order Placed'))
            return redirect('home')

        

    else:
        messages.success(request,('Access Denied'))
        return redirect('home')


def shipping_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        shipped_orders = Order.objects.filter(
            shipping_status=True).order_by('-order_date')
        return render(request,'payment/shipping_dash.html',{"shipped_orders":shipped_orders})
    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')


def unshipping_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        unshipped_orders = Order.objects.filter(
            shipping_status=False).order_by('-order_date')
        return render(request, 'payment/unshipping_dash.html', {"unshipped_orders" : unshipped_orders})
    else:
        messages.success(request, ('Access Denied'))
        return redirect('home')
 