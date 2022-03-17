from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Building Customer Model

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = True,  blank = True)  # models.CASCADE will del the entire item
	name = models.CharField(max_length = 200, null = True)
	email = models.EmailField(max_length = 200, null = True)
	
	def __str__(self):
		return self.name  # Value that shows up in admin panel

# Building Product Model


class Product(models.Model):
	name = models.CharField(max_length = 200, null = True)
	price = models.FloatField(max_length = 6)
	digital = models.BooleanField(default = False, null = True, blank = True)
	image = models.ImageField(null = True, blank = True)  # After adding this, go to settings.py to MEDIA_ROUTE
	
	def __str__(self):
		return self.name
	
	# If there is no img chosen for a product, it crashes the whole page because it is looking for a url
	# So we use this decorator as an attr in store.html to override it with empty url as mentioned in except block
	# property is a decorater that'll let us access a function as an attribute rather than a method
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url  # Now update the img in store.html from product.image.url to product.imageURL

#     Building Order Model


class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
	date_ordered = models.DateTimeField(auto_now_add = True)
	complete = models.BooleanField(default = False)
	transaction_id = models.CharField(max_length = 100, null = True)
	
	def __str__(self):
		return str(self.id)
	
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
			
		return shipping

	@property
	def get_cart_total(self):
		orderItems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderItems])
		return total
	
	@property
	def get_cart_items(self):
		orderItems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderItems])
		return total

#     Building Order Item


class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, blank = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
	quantity = models.IntegerField(default = 0, null = True, blank = True)
	date_ordered = models.DateTimeField(auto_now_add = True)
	
	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True, blank = True)
	order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
	address = models.CharField(max_length = 200, null = True)
	City = models.CharField(max_length = 200, null = True)
	State = models.CharField(max_length = 200, null = True)
	zipcode = models.CharField(max_length = 200, null = True)
	date_added = models.DateTimeField(auto_now_add = True)
	
	def __str__(self):
		return self.address

# Once you've made models, run makemigrations and migrate
# Then go to admin.py to register models
