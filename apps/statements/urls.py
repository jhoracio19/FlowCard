# apps/statements/urls.py
from django.urls import path
from .views import StatementCreateView, MarkAsPaidView, PaymentHistoryView

app_name = 'statements'

urlpatterns = [
    path('add/', StatementCreateView.as_view(), name='add'),
    path('mark-as-paid/<int:pk>/', MarkAsPaidView.as_view(), name='mark_as_paid'),
    path('history/', PaymentHistoryView.as_view(), name='history'),
]