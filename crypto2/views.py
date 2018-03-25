from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("<title></title><head><h1>Cryptocurrency Exchange Simulation</h1></head><body></body>")