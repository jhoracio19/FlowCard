from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse

# Importaciones de modelos desde la app cards
from cards.models import MonthlyStatement, InstallmentPlan 
from .forms import StatementForm

class StatementCreateView(LoginRequiredMixin, CreateView):
    model = MonthlyStatement
    form_class = StatementForm
    template_name = 'statements/statement_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pasamos el usuario para filtrar las tarjetas en el formulario
        kwargs['user'] = self.request.user
        return kwargs

class MarkAsPaidView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # 1. Seguridad: Obtenemos el statement asegurando que la tarjeta sea del usuario
        statement = get_object_or_404(MonthlyStatement, id=pk, card__user=request.user)
        statement.is_paid = True
        statement.save()

        # 2. Lógica de MSI: Avanzar cuota automáticamente
        # Reforzamos el filtro: tarjeta del statement Y que pertenezca al usuario
        related_plans = InstallmentPlan.objects.filter(
            card=statement.card, 
            card__user=request.user,
            is_active=True
        )

        for plan in related_plans:
            if plan.current_installment < plan.total_installments:
                plan.current_installment += 1
                
                # Desactivar si se llega al límite de cuotas
                if plan.current_installment == plan.total_installments:
                    plan.is_active = False
                plan.save()
        
        # Soporte para HTMX (eliminación suave de la fila)
        if request.headers.get('HX-Request'):
            return HttpResponse("") 
        
        return redirect('cards:dashboard')

class PaymentHistoryView(LoginRequiredMixin, ListView):
    model = MonthlyStatement
    template_name = 'statements/payment_history.html'
    context_object_name = 'paid_statements'

    def get_queryset(self):
        # Filtrado de seguridad para el historial
        return MonthlyStatement.objects.filter(
            card__user=self.request.user,
            is_paid=True
        ).order_by('-month_year')