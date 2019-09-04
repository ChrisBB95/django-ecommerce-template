from django.shortcuts import render, get_object_or_404

from django.conf import settings
from .models import Product

def shop(request):

    products = Product.objects.filter(available=True)

    context = {
        'products':products,
    }
    return render(request, 'shop/shop.html', context)


def product(request, item_slug=None):
    
    product = get_object_or_404(
        Product, slug=item_slug, available=True)
    
    context = {
        'product':product,
    }
    return render(request, 'shop/product.html', context)