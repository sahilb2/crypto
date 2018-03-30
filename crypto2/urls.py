from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('<str:currency>_<int:amount>/', views.exchange_currency, name = 'exchange'),
]