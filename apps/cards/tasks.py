from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import MonthlyStatement

def send_payment_reminders():
    # 1. Definimos la fecha objetivo (ej. hoy + 3 días)
    today = timezone.now().date()
    target_date = today + timedelta(days=3)

    print(f"DEBUG: Buscando pagos que vencen el: {target_date}")

    # 2. Filtramos por el campo 'month_year' que es donde guardas la fecha
    upcoming_payments = MonthlyStatement.objects.filter(
        month_year=target_date,  # <-- CAMBIO AQUÍ
        is_paid=False
    )

    print(f"DEBUG: Se encontraron {upcoming_payments.count()} recordatorios.")

    sent_count = 0
    for statement in upcoming_payments:
        user = statement.card.user
        if user.email:
            subject = f'⏳ Recordatorio: Pago de {statement.card.bank_name} vence pronto'
            message = (
                f'Hola {user.username},\n\n'
                f'Te recordamos que el pago de tu tarjeta {statement.card.card_name} '
                f'por un monto de ${statement.non_interest_payment} vence el {statement.month_year}.\n\n'
                f'¡Evita recargos pagando a tiempo!'
            )
            
            send_mail(
                subject,
                message,
                'jhoracioag11@gmail.com',
                [user.email],
                fail_silently=False,
            )
            sent_count += 1
            
    return f"Se enviaron {sent_count} recordatorios."