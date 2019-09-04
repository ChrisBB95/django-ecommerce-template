from django.shortcuts import render

from django.conf import settings
from shop.models import Product
from .models import Order

from paypalrestsdk import Payment
import stripe

def checkout(request):
    context = {}

    return render(request, 'payment/checkout.html', context)

def process(request):
    context = {}

    return render(request, 'payment/process.html', context)

def checkout_complete(request):
    context = {}

    return render(request, 'payment/checkout_complete.html', context)