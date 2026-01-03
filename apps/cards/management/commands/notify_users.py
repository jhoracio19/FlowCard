from django.core.management.base import BaseCommand
from cards.tasks import send_payment_reminders

class Command(BaseCommand):
    help = 'Busca pagos próximos a vencer (T+3 días) y envía correos a los usuarios'

    def handle(self, *args, **options):
        # Usamos style para que la terminal se vea profesional con colores
        self.stdout.write(self.style.WARNING('--- Iniciando Proceso de Notificación ---'))
        
        try:
            resultado = send_payment_reminders()
            self.stdout.write(self.style.SUCCESS(f'OK: {resultado}'))
        except Exception as e:
            # Si algo falla (ej. error de conexión SMTP), lo veremos en rojo
            self.stdout.write(self.style.ERROR(f'ERROR CRÍTICO: {e}'))
        
        self.stdout.write(self.style.WARNING('--- Proceso Finalizado ---'))