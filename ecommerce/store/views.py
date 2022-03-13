from django.shortcuts import render
from .models import *


# Create your views here.

def store(request):
    # After Models, migration, admin and added values by admin

    products = Product.objects.all()

    # Previously
    context = {
        'products': products}  # creating context dictionary to pass objects to template, PS: dict updated, empty previously
    return render(request, 'store/store.html',
                  context)  # dirInTemplate/relevantHtmlFile | context to see that data in there
    # Previously

# After updating views, go to template store.html

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)
