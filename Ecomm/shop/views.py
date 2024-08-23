from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import Product,Category,Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UserUpdateForm,ChangePasswordForm,UserInfoForm
from django.db.models import Q
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingForm
import json
# Create your views here.


def home(request):
    Products = Product.objects.all()
    # username = None

    # if request.user.is_authenticated:
    #     main_user = User.objects.get(id=request.user.id)
    #     username = main_user.username


    return render(request,'home.html',{'products':Products})




def about(request):
    return render(request,'about.html',{})

def search(request):
    # query = request.GET.get('q')

    if request.method == 'POST':

        searched = request.POST['searched']
        products = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched))
        if  not products:
            messages.success(
            request, ('No products found for the given keyword'))
            return render(request,'search.html', {})
        else:
            return render(request, 'search.html', {'products': products})

    else:
        return render(request,'search.html',{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password )

        if user is not None:
            login(request,user)

            current_user = Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            
            cart = Cart(request)
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                for key,val in converted_cart.items():
                    cart.db_add(product=key, quantity=val)
            

            messages.success(request, (f'Welcome {username} you have been logged in....'))
            return redirect('home')

        else:
            messages.success(request, ('something went wrong Try Again'))
            return redirect('login')

    else:
        return render(request,'login.html',{})

def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
        
            messages.success(request, ('Account created for '+ username + ' Please fill out below Infrmation'))
            return redirect('update_info')
        else:
            messages.success(request, ('Something Went wrong...'))
            return redirect('register')
    else:
        return render(request,'register.html',{'form': form})


        
    
def update_user(request):

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UserUpdateForm(request.POST or None,instance = current_user)

        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request, ('Profile updated successfully'))
            return redirect('home')
        
        return render(request,'update_user.html',{'user_form': user_form})
    else:
        messages.success(request, ('You must be logged in to access this page'))
        return redirect('login')
        

    
def update_password(request):

    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,('Your password has been updated'))
                return redirect('login')
                # login(request,current_user)
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
    
            return render(request,'update_password.html',{'form': form})    
    else:
        messages.success(
            request, ('You must be logged in to access this page'))
        return redirect('login')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)

        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)

        info_form = UserInfoForm(request.POST or None, instance=current_user)

        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if info_form.is_valid() or shipping_form.is_valid():
            info_form.save()
            shipping_form.save()
            messages.success(request, ('User Info updated successfully'))
            return redirect('home')

        return render(request, 'update_info.html', {'user_form': info_form , 'shipping_form':shipping_form})
    else:
        messages.success(
            request, ('You must be logged in to access this page'))
        return redirect('login')



def logout_user(request):
    logout(request)
    messages.success(request,(f' you have been logged out....'))
    return redirect('home')


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def category(request,foo):
    foo = foo.replace('-',' ')
    
    try:
        
        category = Category.objects.get(name=foo)
        

        products = Product.objects.filter(category=category)
        
        return render(request, 'category.html', {'category': category, 'products': products})


    except:
        messages.success(request, ('Category doesnt Exist'))
        return redirect('home')


