# apps/cards/urls.py
from django.urls import path
from .views import DashboardView, CreditCardCreateView

app_name = 'cards'
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('cards/add/', CreditCardCreateView.as_view(), name='card_add'), # Nueva ruta
]