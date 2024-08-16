from django.urls import path
from . import views


urlpatterns = [

    path('', views.cart_summary, name='cart_summary'),
    path('add/', views.add_cart, name='cart_add'),
    path('update/', views.update_cart, name='cart_update'),
    # path('delete/', views.delete_cart, name='cart-delete'),


]
