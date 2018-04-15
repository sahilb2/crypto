from django import forms

class SimulationForm(forms.Form):
	amount = forms.IntegerField()
	currency = forms.CharField()
