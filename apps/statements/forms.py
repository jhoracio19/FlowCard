# apps/statements/forms.py
from django import forms
from cards.models import MonthlyStatement, CreditCard

class StatementForm(forms.ModelForm):
    class Meta:
        model = MonthlyStatement
        # Usamos 'month_year' para guardar la fecha límite de pago
        fields = ['card', 'month_year', 'min_payment', 'non_interest_payment']
        labels = {
            'month_year': 'Fecha Límite de Pago',
        }
        widgets = {
            'month_year': forms.DateInput(attrs={
                'type': 'date', # Cambiado de 'month' a 'date'
                'class': 'w-full p-2 border rounded-lg'
            }),
            'card': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'min_payment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'non_interest_payment': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = CreditCard.objects.filter(user=user)
    
    # YA NO NECESITAS el método clean_month_year porque el widget 'date' 
    # envía la fecha en el formato correcto. Puedes borrarlo.