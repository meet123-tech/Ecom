from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import Product

# Create your views here.


def home(request):
    Products = Product.objects.all()
    return render(request,'home.html',{'products':Products})



def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password )

        if user is not None:
            login(request,user)
            messages.success(request, ('you have been logged in....'))
            return redirect('home')

        else:
            messages.success(request, ('something went wrong Try Again'))
            return redirect('login')

    else:
        return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,('you have been logged out....'))
    return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})