import json
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from .models import CreditCard, MonthlyStatement, InstallmentPlan
from .services import get_best_card_to_use
from .forms import CreditCardForm, InstallmentPlanForm
from .forms import CustomUserRegisterForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'cards/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # FILTRADO DE SEGURIDAD: Solo datos del usuario autenticado
        user_cards = CreditCard.objects.filter(user=self.request.user)
        
        # Filtrar estados de cuenta pendientes del usuario
        pending_statements = MonthlyStatement.objects.filter(
            card__user=self.request.user,
            is_paid=False
        ).order_by('due_date')

        # Filtrar planes MSI activos del usuario
        installment_plans = InstallmentPlan.objects.filter(
            card__user=self.request.user,
            is_active=True
        )

        # Lógica de Recomendación
        best_card = get_best_card_to_use(user_cards)
        next_to_pay = pending_statements.first() 
        
        # Datos para Gráfica 1 (Distribución)
        card_labels = [card.bank_name for card in user_cards]
        card_limits = [float(card.credit_limit) for card in user_cards]
        card_colors = [str(card.color).strip() if card.color else '#4f46e5' for card in user_cards]
        
        # Lógica para Gráfica 2 (Salud Financiera)
        total_limit = float(user_cards.aggregate(Sum('credit_limit'))['credit_limit__sum'] or 0)
        statement_debt = float(pending_statements.aggregate(Sum('non_interest_payment'))['non_interest_payment__sum'] or 0)
        current_month_msi = float(installment_plans.aggregate(Sum('monthly_payment'))['monthly_payment__sum'] or 0)
        
        immediate_payment = statement_debt + current_month_msi
        total_remaining_plans = sum(float(plan.remaining_amount) for plan in installment_plans)
        locked_credit = max(0, total_remaining_plans - current_month_msi)
        available_credit = max(0, total_limit - immediate_payment - locked_credit)

        context.update({
            'cards': user_cards,
            'best_card': best_card,
            'next_to_pay': next_to_pay,
            'pending_statements': pending_statements,
            'installment_plans': installment_plans,
            'chart_labels': json.dumps(card_labels),
            'chart_limits': json.dumps(card_limits),
            'chart_colors': json.dumps(card_colors),
            'debt_data': json.dumps([immediate_payment, locked_credit, available_credit])
        })
        return context

# --- VISTAS DE TARJETAS (SEGURIDAD REFORZADA) ---

class CreditCardCreateView(LoginRequiredMixin, CreateView):
    model = CreditCard
    form_class = CreditCardForm
    template_name = 'cards/card_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def form_valid(self, form):
        # Asignar automáticamente el usuario logueado al crear
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreditCardUpdateView(LoginRequiredMixin, UpdateView):
    model = CreditCard
    form_class = CreditCardForm
    template_name = 'cards/card_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def get_queryset(self):
        # El queryset filtrado evita que editen IDs de otros usuarios
        return CreditCard.objects.filter(user=self.request.user)

class CreditCardDeleteView(LoginRequiredMixin, DeleteView):
    model = CreditCard
    success_url = reverse_lazy('cards:dashboard')

    def get_queryset(self):
        # El queryset filtrado evita que borren IDs ajenos
        return CreditCard.objects.filter(user=self.request.user)

# --- VISTAS DE PLANES MSI ---

class InstallmentPlanCreateView(LoginRequiredMixin, CreateView):
    model = InstallmentPlan
    form_class = InstallmentPlanForm
    template_name = 'cards/plan_form.html'
    success_url = reverse_lazy('cards:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user # Pasa el usuario para filtrar el dropdown de tarjetas en el form
        return kwargs

class InstallmentPlanDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # get_object_or_404 con filtro de usuario es la defensa final
        plan = get_object_or_404(InstallmentPlan, id=pk, card__user=request.user)
        plan.delete()
        return redirect('cards:dashboard')


class RegisterView(CreateView):
    form_class = CustomUserRegisterForm # Cambiamos UserCreationForm por el tuyo
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')