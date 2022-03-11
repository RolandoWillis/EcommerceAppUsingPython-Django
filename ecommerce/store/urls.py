from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name = "store"), # home | name is dynamic name
    path('cart/', views.cart, name = "cart"),
    path('checkout/', views.checkout, name = "checkout"),
]