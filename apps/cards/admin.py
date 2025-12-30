from django.contrib import admin
from .models import CreditCard, MonthlyStatement

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'card_name', 'user', 'closing_day')

@admin.register(MonthlyStatement)
class MonthlyStatementAdmin(admin.ModelAdmin):
    list_display = ('card', 'month_year', 'is_paid')