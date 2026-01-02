from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    bank_name = models.CharField(max_length=50)
    card_name = models.CharField(max_length=50, help_text="Ej. Visa Gold")
    color = models.CharField(max_length=7, default="#4f46e5")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Days of the month (1-31)
    closing_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    due_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])

    def __str__(self):
        return f"{self.bank_name} - {self.card_name}"
    
    class Meta:
        app_label = 'cards'

class MonthlyStatement(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='statements')
    month_year = models.DateField(help_text="Mes al que corresponde este estado de cuenta")
    
    # --- AÑADE ESTE CAMPO ---
    due_date = models.DateField(null=True, blank=True, help_text="Fecha límite de pago exacta")
    
    min_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    non_interest_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    
    def days_until_due(self):
        """Calcula cuántos días faltan para la fecha de vencimiento."""
        today = timezone.now().date()
        if self.due_date:
            delta = self.due_date - today
            return delta.days
        return None

    class Meta:
        unique_together = ('card', 'month_year')

    def __str__(self):
        return f"{self.card.card_name} - {self.month_year.strftime('%B %Y')}"

class InstallmentPlan(models.Model):
    PLAN_TYPES = [
        ('MSI', 'Meses sin Intereses'),
        ('FIXED', 'Pagos Fijos / Reestructura'),
    ]
    
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=100, help_text="Ej: iPhone 15 o Reestructura Enero")
    type = models.CharField(max_length=10, choices=PLAN_TYPES, default='MSI')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_installments = models.IntegerField(help_text="Número total de meses")
    current_installment = models.IntegerField(default=1, help_text="En qué mes vas actualmente")
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto a pagar cada mes")
    start_date = models.DateField()
    is_active = models.BooleanField(default=True)

    @property
    def remaining_amount(self):
        return self.total_amount - (self.monthly_payment * (self.current_installment - 1))

    def __str__(self):
        return f"{self.name} ({self.current_installment}/{self.total_installments})"