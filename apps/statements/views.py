# apps/statements/views.py
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from cards.models import MonthlyStatement
from .forms import StatementForm
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView
from cards.models import MonthlyStatement
from django.http import HttpResponse

class StatementCreateView(LoginRequiredMixin, CreateView):
    model = MonthlyStatement
    form_class = StatementForm
    template_name = 'statements/statement_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pasamos el usuario al formulario
        return kwargs

class MarkAsPaidView(LoginRequiredMixin, View):
    def post(self, request, pk):
        statement = get_object_or_404(MonthlyStatement, id=pk, card__user=request.user)
        statement.is_paid = True
        statement.save()
        
        # Si la petición viene de HTMX, devolvemos un contenido vacío
        if request.headers.get('HX-Request'):
            return HttpResponse("") 
        
        # Si no es HTMX (fallback), redirigimos normal
        return redirect('cards:dashboard')

class PaymentHistoryView(LoginRequiredMixin, ListView):
    model = MonthlyStatement
    template_name = 'statements/payment_history.html'
    context_object_name = 'paid_statements'

    def get_queryset(self):
        # Filtramos solo los que YA están pagados del usuario actual
        return MonthlyStatement.objects.filter(
            card__user=self.request.user,
            is_paid=True
        ).order_by('-month_year') # Los más recientes primero