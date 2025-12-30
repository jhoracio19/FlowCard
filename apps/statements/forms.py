# apps/statements/forms.py
from django import forms
from cards.models import MonthlyStatement, CreditCard

class StatementForm(forms.ModelForm):
    class Meta:
        model = MonthlyStatement
        fields = ['card', 'month_year', 'min_payment', 'non_interest_payment']
        widgets = {
            'month_year': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border rounded-lg'}),
            'card': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'min_payment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'non_interest_payment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos para que solo aparezcan las tarjetas del usuario logueado
        self.fields['card'].queryset = CreditCard.objects.filter(user=user)