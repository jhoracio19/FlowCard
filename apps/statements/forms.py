from django import forms
from cards.models import MonthlyStatement, CreditCard
from datetime import date

class StatementForm(forms.ModelForm):
    # Creamos campos extra que no están en el modelo para capturar solo Mes y Año
    MESES = [(i, date(2000, i, 1).strftime('%B').capitalize()) for i in range(1, 13)]
    ANIOS = [(i, i) for i in range(date.today().year, date.today().year + 2)]

    mes = forms.ChoiceField(choices=MESES, initial=date.today().month, label="Selecciona el Mes")
    anio = forms.ChoiceField(choices=ANIOS, initial=date.today().year, label="Año")

    class Meta:
        model = MonthlyStatement
        # Quitamos 'month_year' de los campos visibles, lo manejaremos internamente
        fields = ['card', 'min_payment', 'non_interest_payment']
        labels = {
            'card': 'Tarjeta de Crédito',
            'min_payment': 'Pago Mínimo',
            'non_interest_payment': 'Pago para no generar Intereses',
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['card'].queryset = CreditCard.objects.filter(user=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Construimos la fecha 'month_year' usando el primer día del mes elegido
        mes = int(self.cleaned_data['mes'])
        anio = int(self.cleaned_data['anio'])
        instance.month_year = date(anio, mes, 1) # Guardamos el día 1 como referencia
        
        if commit:
            instance.save()
        return instance