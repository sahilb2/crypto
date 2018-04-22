from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from simTrade import exchange, simulation
import ccxt
from .forms import SimulationForm
import subprocess as sp
import sys

def index(request):
	form = SimulationForm()
	context = {'form': form}
	return render(request, "crypto2/index.html", context)

def print_http_response(f):
    """ Wraps a python function that prints to the console, and
    returns those results as a HttpResponse (HTML)"""

    class WritableObject:
        def __init__(self):
            self.content = []
        def write(self, string):
            self.content.append(string)

    def new_f(*args, **kwargs):
        printed = WritableObject()
        sys.stdout = printed
        f(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return HttpResponse(['<BR>' if c == '\n' else c for c in printed.content ])
    return new_f

@print_http_response
def results(request):
	output = ""
	if request.method == 'POST':
		form = SimulationForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data['amount']
			currency = form.cleaned_data['currency']
			duration = form.cleaned_data['duration']
			sim = simulation.ArbitrageSimulation(ccxt.exmo(), ccxt.gdax(), "BTC/USD")
			sim.start_simulation(duration)
			context = {'form': form,
					   'currency': currency,
					   'amount': amount,
					   'output': output}
			return render(request, "crypto2/results.html", context)
	else:
		form = SimulationForm()
	return render(request, "crypto2/results.html", {'form': form})
		