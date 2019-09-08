from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from django.conf import settings
from .models import Product, add_to_session_cart, add_to_user_cart, remove_from_session_cart, remove_from_user_cart

def products(request):

    products = Product.objects.filter(available=True)

    context = {
        'products':products,
    }
    return render(request, 'shop/shop.html', context)


def product_detail(request, item_slug=None):
    
    product = get_object_or_404(
        Product, slug=item_slug, available=True)
    
    context = {
        'product':product,
    }
    return render(request, 'shop/product.html', context)