from django import forms

BASE_CURRENCY_CHOICES = (
	('BTC', 'Bitcoin'),
	('ETH', 'Etherium'),
	('LTC', 'LiteCoin'),
)
QUOTE_CURRENCY_CHOICES = (
	('USD', 'US Dollar'),
)
USE_FEES = (
	(True, 'Yes'),
	(False, 'No'),
)
class SimulationForm(forms.Form):
	base_currency = forms.ChoiceField(choices=BASE_CURRENCY_CHOICES)
	quote_currency = forms.ChoiceField(choices=QUOTE_CURRENCY_CHOICES)
	amount = forms.FloatField()
	duration = forms.FloatField()
	include_fees = forms.ChoiceField(choices=USE_FEES)