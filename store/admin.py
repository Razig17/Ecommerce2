from django.contrib import admin
from .models import Category, Product, Customer, Order,OrderItem
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
# show customer info with the user info in the admin panel

class InfoInline(admin.StackedInline):
    model = Customer

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    inlines = [InfoInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
