from django.shortcuts import render
from django.conf import settings

def home(request):
    context = {}

    return render(request, 'home/home.html', context)
    
def contact(request):
    context = {}

    return render(request, 'home/contact.html', context)

def cart(request):
    context = {}

    return render(request, 'home/cart.html', context)