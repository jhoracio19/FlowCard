from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    bank_name = models.CharField(max_length=50)
    card_name = models.CharField(max_length=50, help_text="Ej. Visa Gold")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Days of the month (1-31)
    closing_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    due_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])

    def __str__(self):
        return f"{self.bank_name} - {self.card_name}"

class MonthlyStatement(models.Model):
    card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name='statements')
    month_year = models.DateField(help_text="First day of the billing month")
    min_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    non_interest_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('card', 'month_year')

    def __str__(self):
        return f"{self.card.card_name} - {self.month_year.strftime('%B %Y')}"