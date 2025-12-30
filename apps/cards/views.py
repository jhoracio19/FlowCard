# apps/cards/views.py
import json
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy

from .models import CreditCard, MonthlyStatement
from .services import get_best_card_to_use
from .forms import CreditCardForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_cards = CreditCard.objects.filter(user=self.request.user)
        
        # --- Datos para Gráfica 1: Distribución ---
        card_labels = [card.bank_name for card in user_cards]
        card_limits = [float(card.credit_limit) for card in user_cards]
        
        # --- Datos para Gráfica 2: Deuda vs Disponible ---
        total_limit = float(user_cards.aggregate(Sum('credit_limit'))['credit_limit__sum'] or 0)
        # Sumamos los pagos para no generar intereses del mes actual de todas las tarjetas
        total_debt = float(MonthlyStatement.objects.filter(
            card__user=self.request.user, 
            is_paid=False
        ).aggregate(Sum('non_interest_payment'))['non_interest_payment__sum'] or 0)
        
        available_credit = max(0, total_limit - total_debt)

        context.update({
            'cards': user_cards,
            'best_card': get_best_card_to_use(user_cards),
            # Pasamos los datos como JSON para JS
            'chart_labels': json.dumps(card_labels),
            'chart_limits': json.dumps(card_limits),
            'debt_data': json.dumps([total_debt, available_credit])
        })
        return context

class CreditCardCreateView(LoginRequiredMixin, CreateView):
    model = CreditCard
    form_class = CreditCardForm
    template_name = 'cards/card_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)