from django import forms

class SimulationForm(forms.Form):
	amount = forms.FloatField()
	currency = forms.CharField()
	duration = forms.FloatField()
