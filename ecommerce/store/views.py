from django.shortcuts import render

# Create your views here.

def store(request):
    context = {}    # creating context dictionary to pass some data
    return render(request, 'store/store.html', context) # dirInTemplate/relevantHtmlFile | context to see that data in there

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)