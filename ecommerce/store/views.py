from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json



# Create your views here.

def store(request):
    # After Models, migration, admin and added values by admin

    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer, complete=False)  # get_or_create() => Queries an obj with certain val, if it doesn't exist, it creates it
        items = order.orderitem_set.all() # Getting All the orderitems that have a certain order as parent | we can query child obj by setting the parent val & then the child obj with all lowercase values
        cartItems = order.get_cart_items
    else:
        # if user is not logged in, the page crashes as there is no values to be retrieved on template so we create a manual dict
        items = []
        order = {'get_cart_total': 0,'get_cart_items': 0}
        cartItems = order['get_cart_items']

    # Previously
    context = {
        'products': products, 'cartItems': cartItems}  # creating context dictionary to pass objects to template, PS: dict updated, empty previously
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


def updateItem(request):
    data = json.loads(request.body)  # we're passing in that data and now printing it out
    productId = data['productId']
    action = data['action']
    print("Action:", action)
    print("Product ID:", productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # get_or_create() is used because if an item already exists in cart,
    # we dont wanna create it again, we just wanna update the quantity of it

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
