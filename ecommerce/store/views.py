from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):
	# After Models, migration, admin and added values by admin
	
	data = cartData(request)
	cartItems = data['cartItems']
	
	products = Product.objects.all()
	context = {'products': products, 'cartItems': cartItems}  # creating context dictionary to pass objects to template, PS: dict updated, empty previously
	return render(request, 'store/store.html', context)  # dirInTemplate/relevantHtmlFile | context to see that data in there

# After updating views, go to template store.html

def cart(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	context = {'items': items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)  # we're passing in that data and now printing it out
	productId = data['productId']
	action = data['action']
	print("Action:", action)
	print("Product ID:", productId)
	customer = request.user.customer
	product = Product.objects.get(id = productId)
	
	# get_or_create() is used because if an item already exists in cart,
	# we don't wanna create it again, we just wanna update the quantity of it
	
	order, created = Order.objects.get_or_create(customer = customer, complete = False)
	orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
	
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	
	orderItem.save()
	
	if orderItem.quantity <= 0:
		orderItem.delete()
	
	return JsonResponse('Item was added', safe = False)

# When a new user logs in("incognito"), he gets a forbidden:403 error as it doesn't build session for some reason
# To cater this, we have a quick fix here in which we use csrf_exempt which is builtin decorator
# csrf_exempt: whenever POST data gets sent to the checkout view, we don't need a csrf token

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt

# This was 1 way for data with no security issues
# The secure way is that we add a csrf token in form in checkout.html


def processOrder(request):
	# print('Data:', request.body)
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	
	# for authenticated user
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer, complete = False)
	
	# For Non-authenticated user
	else:
		customer, order = guestOrder(request, data)  # in utils.py
			
	# Confirming total for both authenticated and anon user
	
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	
	# Checking if total = Cart Total
	
	if total == float(order.get_cart_total):
		order.complete = True
	order.save()
	
	# Setting Shipping Form for both authenticated and anon user
	
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			zipcode = data['shipping']['zipcode'],
		)
	
	return JsonResponse('Payment Successful', safe = False)
