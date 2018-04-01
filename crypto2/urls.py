from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('currency=<str:currency>&amount=<int:amount>/', views.exchange_currency, name = 'exchange'),
]