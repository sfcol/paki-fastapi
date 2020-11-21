from django.shortcuts import render

from api.models import Product


def home(request):
    products = Product.objects.all()
    return render(request, "./api/home.html", {'list': products})
