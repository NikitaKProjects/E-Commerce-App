from django.shortcuts import render

# Create your views here.
def get_products(request, slug):
    return render(request, "products/products.html")
