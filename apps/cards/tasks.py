from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from .models import MonthlyStatement

def send_payment_reminders():
    # 1. Definimos el rango de tiempo (3 días para capturar el 5 de enero si hoy es 2)
    today = timezone.now().date()
    target_date = today + timedelta(days=2)

    print(f"DEBUG: Buscando pagos para la fecha: {target_date}")

    # 2. Buscamos statements pendientes con fecha exacta y no pagados
    upcoming_payments = MonthlyStatement.objects.filter(
        due_date=target_date,
        is_paid=False
    )

    print(f"DEBUG: Se encontraron {upcoming_payments.count()} registros coincidentes.")

    sent_count = 0
    for statement in upcoming_payments:
        user = statement.card.user
        if user.email:
            subject = f'⏳ Recordatorio: Pago de {statement.card.bank_name} vence pronto'
            message = (
                f'Hola {user.username},\n\n'
                f'Te recordamos que el pago de tu tarjeta {statement.card.card_name} '
                f'por un monto de ${statement.non_interest_payment} vence el {statement.due_date}.\n\n'
                f'¡Evita recargos pagando a tiempo!'
            )
            
            # El remitente debe ser el mismo configurado en EMAIL_HOST_USER
            send_mail(
                subject,
                message,
                'jhoracioag11@gmail.com', # Asegúrate de que este sea tu EMAIL_HOST_USER
                [user.email],
                fail_silently=False,
            )
            sent_count += 1
            print(f"DEBUG: Correo enviado a {user.email}")
            
    return f"Se enviaron {sent_count} recordatorios."