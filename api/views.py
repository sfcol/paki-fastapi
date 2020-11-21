from django.shortcuts import render

# Create your views here.
from api.models import Product


def home(request):
   list = Product.objects.all()
   return render(request, "./api/home.html", {'list': list})