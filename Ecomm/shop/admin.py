from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)


# mix profile info and user info

class ProfileInline(admin.StackedInline):
    model = Profile
    


class UserAdmin(admin.ModelAdmin):
    model = User
    feilds = ['username', 'email', 'first_name', 'last_name']
    inlines = [ProfileInline]


admin.site.unregister(User)

admin.site.register(User, UserAdmin)


