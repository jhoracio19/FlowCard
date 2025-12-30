# apps/cards/forms.py
from django import forms
from .models import InstallmentPlan, CreditCard
class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['bank_name', 'card_name', 'credit_limit', 'closing_day', 'due_day']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Ej. BBVA'}),
            'card_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Ej. Visa Platinum'}),
            'credit_limit': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'closing_day': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 1, 'max': 31}),
            'due_day': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg', 'min': 1, 'max': 31}),
        }

class InstallmentPlanForm(forms.ModelForm):
    class Meta:
        model = InstallmentPlan
        fields = [
            'card', 'name', 'type', 'total_amount', 
            'total_installments', 'current_installment', 
            'monthly_payment', 'start_date'
        ]
        widgets = {
            'card': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'name': forms.TextInput(attrs={'placeholder': 'Ej. Laptop Work', 'class': 'w-full p-2 border rounded-lg'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'total_amount': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'total_installments': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'current_installment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'monthly_payment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo mostrar tarjetas del usuario logueado
        self.fields['card'].queryset = CreditCard.objects.filter(user=user)