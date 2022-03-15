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

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)  # get_or_create() => Queries an obj with certain val, if it doesn't exist, it creates it
        items = order.orderitem_set.all() # Getting All the orderitems that have a certain order as parent | we can query child obj by setting the parent val & then the child obj with all lowercase values
    else:
        # if user is not logged in, the page crashes as there is no values to be retrieved on template so we create a manual dict
        items = []
        order = {'get_cart_total': 0,'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)  # get_or_create() => Queries an obj with certain val, if it doesn't exist, it creates it
        items = order.orderitem_set.all() # Getting All the orderitems that have a certain order as parent | we can query child obj by setting the parent val & then the child obj with all lowercase values
    else:
        # if user is not logged in, the page crashes as there is no values to be retrieved on template so we create a manual dict
        items = []
        order = {'get_cart_total': 0,'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)
