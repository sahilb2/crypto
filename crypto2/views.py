from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from . import exchange

def index(request):
	"""
	button = "<button class=""button"">Submit</button>"
	input_curr = "Currency: <input type=""text"" name=""currency"">"
	input_amount = "Amount: <input type=""text"" name=""amount"">"
	body = "<body>" + "<form>" + input_curr + "<br>" + input_amount + "<br>" + button + "</form>" + "</body>"
	response = "<!DOCTYPE html><html><title></title><head><h1>Cryptocurrency Exchange Simulation</h1></head>" + body + "</html>"
	"""
	template = loader.get_template('crypto2/index.html')
	context = {}
	return HttpResponse(template.render(context, request))

def exchange_currency(request, currency, amount):
	binance = exchange.Exchange("binance")
	binance.deposit(currency, amount)
	
	button = "<button class=""button"">Submit</button>"
	input = "<input id = 'currency'>currency:</input>"
	body = "<body>" + str(amount) + " " + currency + " has been deposited" + "<form>" + input + button + "</form>" + "</body>"
	response = "<!DOCTYPE html><html><title></title><head><h1>Cryptocurrency Exchange Simulation</h1></head>" + body + "</html>"
	return HttpResponse(response)