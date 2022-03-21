# This file contains the logics as functions that needs to be repeated in multiple function. So instead of
# repeating, we created this file, will create that logic in a function and use that function as a utility
# Follows DRY Principle, Don't Repeat Yourself

import json
from .models import *


""" For Views.py """

def cookieCart(request):
	
	try:
		cart = json.loads(request.COOKIES['cart'])
		print('Cart:', cart)
		
	except:
		cart = {}
		
	items = []
	order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
	cartItems = order['get_cart_items']
	
	for i in cart:
		# We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]["quantity"]
			
			# Setting total and Items for non-logged in user
			
			product = Product.objects.get(id = i)
			total = (product.price * cart[i]["quantity"])
			
			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]["quantity"]
			
			# Setting Items in cart for non logged in user
			
			item = {'product': {
				'id': product.id,
				'name': product.name,
				'price': product.price,
				'imageURL': product.imageURL,
			},
				
				'quantity': cart[i]["quantity"],
				'get_total': total,
			}
			items.append(item)
			
			if product.digital == False:
				order['shipping'] = True
		
		except:
			pass
		
	return {'cartItems': cartItems, 'order': order, 'items': items}

# To make this function available in our respective file(here views.py) use "from . utils import cookieCart"


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer = customer,
		                                             complete = False)  # get_or_create() => Queries an obj with certain val, if it doesn't exist, it creates it
		items = order.orderitem_set.all()  # Getting All the orderitems that have a certain order as parent | we can query child obj by setting the parent val & then the child obj with all lowercase values
		cartItems = order.get_cart_items
	
	# if user is not logged in, the page crashes as there is no values
	# to be retrieved on template, so we create a manual dictionary
	
	else:
		cookieData = cookieCart(request)  # in utils.py
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']
		
	return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
	print("User is not Logged In")
	print("Cookies:", request.COOKIES)
	
	name = data['form']['name']
	email = data['form']['email']
	
	cookieData = cookieCart(request)
	items = cookieData['items']
	customer, created = Customer.objects.get_or_create(
		email = email,
	)
	
	customer.name = name
	customer.save()
	
	order = Order.objects.create(
		customer = customer,
		complete = False,
	)
	
	for item in items:
		product = Product.objects.get(id = item['product']['id'])
		orderItem = OrderItem.objects.create(
			product = product,
			order = order,
			quantity = item['quantity']
		)

	return customer, order
