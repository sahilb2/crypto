from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from simTrade import exchange, simulation
from .forms import SimulationForm

def index(request):
	form = SimulationForm()
	context = {'form': form}
	return render(request, "crypto2/index.html", context)

def results(request):
	if request.method == 'POST':
		form = SimulationForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data['amount']
			currency = form.cleaned_data['currency']
			binance = exchange.Exchange("binance")
			binance.deposit(currency, amount)
			context = {'form': form,
					   'currency': currency,
					   'amount': amount}
			return render(request, "crypto2/results.html", context)
	else:
		form = SimulationForm()
	return render(request, "crypto2/results.html", {'form': form})
		