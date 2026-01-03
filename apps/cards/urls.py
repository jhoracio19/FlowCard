from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = 'cards'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add/', views.CreditCardCreateView.as_view(), name='card_add'),
    path('edit/<int:pk>/', views.CreditCardUpdateView.as_view(), name='card_edit'),
    path('delete/<int:pk>/', views.CreditCardDeleteView.as_view(), name='card_delete'),
    path('plans/add/', views.InstallmentPlanCreateView.as_view(), name='plan_add'),
    path('plan/<int:pk>/delete/', views.InstallmentPlanDeleteView.as_view(), name='plan_delete'),

]