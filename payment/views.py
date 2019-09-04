from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core import mail

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

@csrf_exempt
def checkout_complete(request):
    context = {}

    return render(request, 'payment/checkout_complete.html', context)

@csrf_exempt
def checkout_canceled(request):
    context = {}

    return render(request, 'payment/checkout_canceled.html', context)