"""Shopng cart class"""
from decimal import Decimal

class Cart():
    """
    A class to represent a shopping cart.
    """
    def __init__(self, request):
        """
        Initializes the Cart object.

        Args:
            request (HttpRequest): The HTTP request object.

        Attributes:
            session (Session): The session object to store cart data.
            cart (dict): The dictionary to store cart items.
        """
        self.session = request.session
        cart = self.session.get("cart")
        if "cart" not in request.session:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add_item(self, item, quantity):
        """
        Adds an item to the cart or updates its quantity if it already exists.

        Args:
            item (Product): The product to add to the cart.
            quantity (int): The quantity of the product to add.
        """
        item_id = str(item.id)

        if item_id not in self.cart:
            self.cart[item_id] = {"id": item.id, "quantity": int(quantity), "price": float(item.price), "name": item.name, "image": item.image.url}
        else:
            
            self.cart[item_id]["quantity"] += int(quantity)
        self.save()

    def remove_item(self, item):
        """
        Removes an item from the cart.

        Args:
            item (Product): The product to remove from the cart.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        """
        Calculates the total price of all items in the cart.

        Returns:
            Decimal: The total price of all items in the cart.
        """
        return sum(item["price"] * item["quantity"] for item in self.cart.values())
    
    def update_quantity(self, item, quantity):
        """
        Updates the quantity of an item in the cart.

        Args:
            item (Product): The product to update the quantity for.
            quantity (int): The new quantity of the product.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            self.cart[item_id]["quantity"] = quantity
            self.save()
    
    def clear(self):
        """
        clears the cart in the session.
        """
        self.session["cart"] = {}
        self.save()

    def save(self):
        """
        Saves the cart data to the session.
        """
        self.session.modified = True

    def __len__(self):
        """
        Returns the total number of items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_items(self):
        """
        Returns the total number of items in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())
