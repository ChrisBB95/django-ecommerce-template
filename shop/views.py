from django.shortcuts import render

from django.conf import settings
from .models import Product

def shop(request):

    context = {}
    return render(request, 'shop/shop.html', context)


def product(request, item_slug=None):
    
    product = Product.objects.filter(slug=item_slug).first()
    
    context = {
        'product':product,
    }
    return render(request, 'shop/product.html', context)