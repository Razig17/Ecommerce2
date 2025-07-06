"""
This module contains the views for the store application, which handles the HTTP requests and return responses.
"""
from django.shortcuts import render, redirect
from .models import Product, Customer, OrderItem, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, CustomerForm ,UserForm, OrderForm
from .cart import Cart
from django.http import JsonResponse

def index(request):
    """
    View function for the home page.
    """
    smartphones = Product.objects.filter(category__name="smartphones")[:4]
    laptops = Product.objects.filter(category__name="laptops")[:4]
    return render(request, "home.html" , {"products": smartphones, "laptops": laptops})


def store(request):
    """
    View function for the store page.
    """
    query = request.GET.get('query', (""))
    category = request.GET.get('category', 0)
    if category == "0":
        products = Product.objects.filter(name__contains=query)
    elif category != 0:
        products = Product.objects.filter(category__name=category, name__contains=query)
    else:
        products = Product.objects.all()
    return render(request, "store.html" , {"products": products})


def smartphones(request):
    """
    View function for the smartphones page.
    """
    products = Product.objects.filter(category__name="smartphones")
    return render(request, "smartphones.html" , {"products": products})


def laptops(request):
    """
    View function for the laptops page
    """
    products = Product.objects.filter(category__name="laptops")
    return render(request, "laptops.html" , {"products": products})


def product(request, id):
    """
    View function for the product page.
    """
    product = Product.objects.get(id=id)
    return render(request, "product.html" , {"product": product})



def login_user(request):
    """
    View function for the login page.
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("store")
        else:
            messages.success(request, "Invalid credentials")
            return redirect("login")
    format = RegisterForm()
    return render(request, "login.html" , {"form": format})


def logout_user(request):
    """
    View function for logging out the user.
    """
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("store")


def register_user(request):
    """
    View function for the registration page.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You’ve successfully registered! Please complete your profile")
            return redirect("my_account")
        else:
            messages.error(request, "Please correct the error .")
    else:
        form = RegisterForm()
    return render(request, "login.html" , {"form": form})


def my_account(request):
    """
    View function for the account page
    """
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in")
        return redirect("login")
    
    elif request.method == 'POST':
        user = Customer.objects.get(user__id=request.user.id)   
        form = CustomerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated")
        else:
            for msg in form.errors:
                messages.error(request, msg)
                messages.error(request, form.errors[msg])
    
    user = Customer.objects.get(user__id=request.user.id)
    user_form = UserForm(instance=request.user)        
    form = CustomerForm(instance=user)
    return render(request, "my_account.html" , {"form": form , "user_form": user_form})


def cart(request):
    """
    View function for the cart page.
    """
    return render(request, "cart.html" , {})


def add_to_cart(request, id):
    """
    View function for adding a product to the cart.
    """
    if request.method == "POST":    
        qty = request.POST.get('qty', 1)
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.add_item(product, (qty))
        msg = 'Product added to cart'
        if int(qty) > 1:
            msg = 'Products added to cart'
        return JsonResponse({"qty": cart.__len__(), "total_price": cart.get_total_price(), "msg": msg})
    

def remove_from_cart(request, id):
    """
    View function for removing a product from the cart.
    """
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove_item(product)
    messages.success(request, "Product removed from cart")
    return redirect("cart")


def update_cart(request, id):
    """
    View function for updating the quantity of a product in the cart.
    """
    if request.method == "POST":
        qty = request.POST.get('qty', 1)
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.update_quantity(product, int(qty))
        msg = 'Product quantity updated'
        return JsonResponse({"total_price": cart.get_total_price(), "msg": msg, "qty": cart.__len__()})


def clear_cart(request):
    """
    View function for clearing the cart.
    """
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Cart cleared")
    return redirect("cart")


def checkout(request):
    """
    View function for the checkout page.
    """
    cart = Cart(request)
    error = None
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.user = None
            order.amount = cart.get_total_price()
            order.save()
            for item in cart.cart.values():
                order_item = OrderItem(order=order, product=Product.objects.get(id=item["id"]), quantity=item["quantity"], price=item["price"])
                order_item.save()
            cart.clear()
            messages.success(request, "Order placed successfully")
            return redirect("store")
        else:
            error = str(form.errors.as_text())   
    if cart.__len__() == 0:
        return JsonResponse({"msg": "Your cart is empty!"})
    else:
        form = OrderForm()
        if request.user.is_authenticated:
            user = Customer.objects.get(user__id=request.user.id)
            form = OrderForm(initial={"full_name": f"{user.user.first_name} {user.user.last_name}", "email": user.user.email, "address": user.address, "phone": user.phone, "city": user.city, "zip_code": user.postal_code})
        return render(request, "checkout.html" , {"form": form, "error": error})
    

def update_user(request):
    """
    View function for updating user information.
    """
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Account updated")
        else:
            for msg in form.errors:
                messages.error(request, msg)
                messages.error(request, form.errors[msg])
            return redirect("my_account")
    return redirect("my_account")



def wishlist(request):
    """
    View function for the wish list page.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"msg": "You need to be logged in to view your wish list"})
    user = Customer.objects.get(user__id=request.user.id)
    product_ids = user.wishlist.keys()
    products = Product.objects.filter(id__in=product_ids)
    return render(request, "wishlist.html", {"products": products})


def add_to_wishlist(request, id):
    """
    View function for adding a product to the wish list.
    """
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "You need to be logged in to add items to the wish list"})
        user = Customer.objects.get(user__id=request.user.id)
        if str(id) in user.wishlist:
            return JsonResponse({"error": "Product already in wishlist"})
        user.wishlist[str(id)] = 1
        user.save()
        return JsonResponse({"msg": "Product added to wishlist", "qty": len(user.wishlist)})
    return render(request, "wishlist.html" , {})


def remove_from_wishlist(request, id):
    """
    View function for removing a product from the wish list.
    """
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"msg": "You need to be logged in to remove items from the wish list"})
        user = Customer.objects.get(user__id=request.user.id)
        if str(id) not in user.wishlist:
            return JsonResponse({"msg": "Product not in wishlist"})
        del user.wishlist[str(id)]
        user.save()
        return redirect("wishlist")
    return redirect("wishlist")

def clear_wishlist(request):
    """
    View function for clearing the wish list.
    """
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"msg": "You need to be logged in to clear the wish list"})
        user = Customer.objects.get(user__id=request.user.id)
        user.wishlist = {}
        user.save()
        redirect("store")
    return redirect("wishlist")
