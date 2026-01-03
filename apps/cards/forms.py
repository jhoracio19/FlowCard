# apps/cards/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InstallmentPlan, CreditCard
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['bank_name', 'card_name', 'color', 'credit_limit', 'closing_day', 'due_day']
        widgets = {
            'bank_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Ej. BBVA'}),
            'card_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg', 'placeholder': 'Ej. Oro'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'w-full h-10 border rounded-lg cursor-pointer'}),
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
            'name': forms.TextInput(attrs={'placeholder': 'Ej. MacBook Pro', 'class': 'w-full p-2 border rounded-lg'}),
            'type': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'total_amount': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'total_installments': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'current_installment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'monthly_payment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = CreditCard.objects.filter(user=user)

class CustomUserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Un correo electrónico válido.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Buscamos si ya existe un usuario con este correo
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Este correo electrónico ya está registrado. Por favor, utiliza otro."
            )
        return email