from django.contrib import admin
from .models import *                   # . represents this directory

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# After registering, create a super user in terminal
# Once created, the next step is to render the added products on site
# To render, go to views




