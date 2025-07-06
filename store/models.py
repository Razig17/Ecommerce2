"""
This file contains the models for the store app.
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save


class Category(models.Model):
    """
    A model for storing product categories
    """
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        """
        Returns the name of the category to be displayed in the admin panel
        """
        return self.name
    
    class Meta:
        """
        Meta class to specify the plural name of the model in the admin panel
        """
        verbose_name_plural = 'categories'


class Product(models.Model):
    """
    A model for storing products
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    details = models.TextField(blank=True, default="")
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product/images/', default='images/default.jpg')

    def __str__(self):
        """
        Returns the name of the product to be displayed in the admin panel
        """
        return self.name
    
    def is_available(self):
        """
        Returns True if the product is in stock, False otherwise
        """
        return self.stock > 0
    

class Customer(models.Model):
    """
    A model for storing customer information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    wishlist = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        """
        Returns the username of the customer to be displayed in the admin panel
        """
        return self.user.username


class Order(models.Model):
    """
    A model for storing order information
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)   
    created_at = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    completed = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10 ,blank=True, null=True)
    is_shipped = models.BooleanField(default=False)
    shipped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """
        Returns the ID of the order to be displayed in the admin panel
        """
        return str(self.id)


class OrderItem(models.Model):
    """
    A model for storing order items
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        """
        Returns the name of the order item to be displayed in the admin panel
        """
        return f"Order item {self.product.name} for order {self.order.id}"


def create_customer(sender, instance, created, **kwargs):
    """
    Create a signal to create a customer when a user is created
    """
    if created:
        customer = Customer(user=instance)
        customer.save()

# Connect the signal to the User model
post_save.connect(create_customer, sender=User)
