from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from simTrade import exchange, simulation
import ccxt
from .forms import SimulationForm
from io import StringIO
import sys

def index(request):
	form = SimulationForm()
	context = {'form': form}
	return render(request, "crypto2/index.html", context)

def results(request):
	output = ""
	if request.method == 'POST':
		form = SimulationForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data['amount']
			base_currency = form.cleaned_data['base_currency']
			quote_currency = form.cleaned_data['quote_currency']
			duration = form.cleaned_data['duration']
			use_fees = form.cleaned_data['include_fees']
			sim = simulation.ArbitrageSimulation(ccxt.exmo(), ccxt.gdax(), amount, base_currency + "/" + quote_currency)
			old_stdout = sys.stdout
			result = StringIO()
			sys.stdout = result
			sim.start_simulation(duration, include_fees=use_fees)
			sim.create_trade_visuals()
			sys.stdout = old_stdout
			result_list = result.getvalue().split("\n")
			result_string = []
			for s in result_list:
				if s is not "":
					result_string.append(s)
			output = result_string
			context = {'form': form,
					   'duration': duration,
					   'amount': amount,
					   'output': output}
			return render(request, "crypto2/results.html", context)
	else:
		form = SimulationForm()
	return render(request, "crypto2/index.html", {'form': form})
		