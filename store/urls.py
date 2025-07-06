"""
This module contains the URL patterns for the store application, mapping
URLs to their corresponding view functions.

Each URL pattern is associated with a view function that handles the
request and returns a response.
"""

from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("store/", views.store, name="store"),
    path("store/smartphones", views.smartphones, name="smartphones"),
    path("store/laptops", views.laptops, name="laptops"),
    path("store/<int:id>", views.product, name="product"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("my_account/", views.my_account, name="my_account"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:id>", views.add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("update_cart/<int:id>", views.update_cart, name="update_cart"),
    path("clear_cart/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_user/", views.update_user, name="update_user"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("add_to_wishlist/<int:id>", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove_from_wishlist/<int:id>", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("clear_wishlist/", views.clear_wishlist, name="clear_wishlist"),
]
