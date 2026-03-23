from django.shortcuts import render, get_object_or_404
from catalog.models import Product

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'catalog/product_detail.html', {'product': product})