"""Context processors for the store app."""
from .cart import Cart
from .models import Customer


def cart(request):
    """
    Context processor to add the cart to the context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the cart.
    """
    return {"cart": Cart(request)}

def wishlist(request):
    """
    Context processor to add the wishlist count to the context.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary containing the wishlist count.
    """
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        return {"wishlist": len(customer.wishlist)}
    return {"wishlist": 0}
