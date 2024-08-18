from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .models import Product,Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UserUpdateForm

# Create your views here.


def home(request):
    Products = Product.objects.all()
    username = None
    
    if request.user.is_authenticated:
        main_user = User.objects.get(id=request.user.id)
        username = main_user.username


    return render(request,'home.html',{'products':Products,'main_user':username })



def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password )

        if user is not None:
            login(request,user)
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
        
            messages.success(request, ('Account created for '+ username))
            return redirect('home')
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


