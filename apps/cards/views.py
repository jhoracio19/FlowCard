# apps/cards/views.py
import json
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

from .models import CreditCard, MonthlyStatement, InstallmentPlan
from .services import get_best_card_to_use
from .forms import CreditCardForm, InstallmentPlanForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Datos base
        user_cards = CreditCard.objects.filter(user=self.request.user)
        pending_statements = MonthlyStatement.objects.filter(
            card__user=self.request.user,
            is_paid=False
        ).order_by('month_year')
        installment_plans = InstallmentPlan.objects.filter(
            card__user=self.request.user,
            is_active=True
        )

        # 2. Recomendación
        best_card = get_best_card_to_use(user_cards)
        
        # 3. Datos Gráfica 1 (Distribución)
        card_labels = [card.bank_name for card in user_cards]
        card_limits = [float(card.credit_limit) for card in user_cards]
        
        # 4. Lógica Matemática para Gráfica 2 (Salud Financiera)
        total_limit = float(user_cards.aggregate(Sum('credit_limit'))['credit_limit__sum'] or 0)
        
        # A. PAGO INMEDIATO (Rojo): Deuda de estados de cuenta + mensualidades de MSI de este mes
        statement_debt = float(pending_statements.aggregate(Sum('non_interest_payment'))['non_interest_payment__sum'] or 0)
        current_month_msi = float(installment_plans.aggregate(Sum('monthly_payment'))['monthly_payment__sum'] or 0)
        immediate_payment = statement_debt + current_month_msi

        # B. SALDO RETENIDO/GRIS: Todo el capital de MSI que aún no vence (excluyendo el pago de este mes)
        # Usamos la propiedad remaining_amount que definimos en el modelo
        total_remaining_plans = sum(float(plan.remaining_amount) for plan in installment_plans)
        locked_credit = max(0, total_remaining_plans - current_month_msi)
        
        # C. CRÉDITO DISPONIBLE (Verde): Lo que sobra del límite total
        available_credit = max(0, total_limit - immediate_payment - locked_credit)

        # 5. Actualizar el contexto
        context.update({
            'cards': user_cards,
            'best_card': best_card,
            'pending_statements': pending_statements,
            'installment_plans': installment_plans,
            'chart_labels': json.dumps(card_labels),
            'chart_limits': json.dumps(card_limits),
            # Enviamos los 3 valores: [Urgente, Retenido, Libre]
            'debt_data': json.dumps([immediate_payment, locked_credit, available_credit])
        })
        return context

# ... el resto de las vistas (CreditCardCreateView, RegisterView, InstallmentPlanCreateView) se mantienen igual
class CreditCardCreateView(LoginRequiredMixin, CreateView):
    model = CreditCard
    form_class = CreditCardForm
    template_name = 'cards/card_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class InstallmentPlanCreateView(LoginRequiredMixin, CreateView):
    model = InstallmentPlan
    form_class = InstallmentPlanForm
    template_name = 'cards/plan_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs