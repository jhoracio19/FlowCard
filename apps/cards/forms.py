# apps/cards/forms.py
from django import forms
from .models import CreditCard

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