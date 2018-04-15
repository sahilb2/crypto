from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('results/', views.exchange_currency, name = 'exchange'),
]