from django.urls import path
from . import views


urlpatterns = [

    path('payment_success', views.payment_success, name='payment_success'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_Info', views.billing_info, name='billing_info'),
    path('process_order', views.process_order, name='process_order'),
    path('shipping_dash', views.shipping_dash, name='shipping_dash'),
    path('unshipping_dash', views.unshipping_dash, name='unshipping_dash'),



    

    


]