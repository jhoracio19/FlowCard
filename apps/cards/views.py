# apps/cards/views.py
import json
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from .models import CreditCard, MonthlyStatement
from .services import get_best_card_to_use
from .forms import CreditCardForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Obtener datos base del usuario
        user_cards = CreditCard.objects.filter(user=self.request.user)
        
        # 2. Obtener pagos pendientes (is_paid=False)
        # Los ordenamos por fecha de mes para ver los más antiguos primero
        pending_statements = MonthlyStatement.objects.filter(
            card__user=self.request.user,
            is_paid=False
        ).order_by('month_year')
        
        # 3. Lógica de Recomendación (Mejor tarjeta para usar hoy)
        best_card = get_best_card_to_use(user_cards)
        
        # 4. Datos para Gráfica 1: Distribución de Límites de Crédito
        card_labels = [card.bank_name for card in user_cards]
        card_limits = [float(card.credit_limit) for card in user_cards]
        
        # 5. Datos para Gráfica 2: Salud Financiera (Deuda vs Disponible)
        total_limit = float(user_cards.aggregate(Sum('credit_limit'))['credit_limit__sum'] or 0)
        
        # Sumamos la deuda de todos los estados de cuenta NO pagados
        total_debt = float(pending_statements.aggregate(
            Sum('non_interest_payment')
        )['non_interest_payment__sum'] or 0)
        
        available_credit = max(0, total_limit - total_debt)

        # 6. Actualizar el contexto para el Template
        context.update({
            'cards': user_cards,
            'best_card': best_card,
            'pending_statements': pending_statements,
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
        # Asignamos automáticamente el usuario logueado a la tarjeta creada
        form.instance.user = self.request.user
        return super().form_valid(form)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')