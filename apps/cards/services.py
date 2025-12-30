from datetime import date, timedelta

def get_best_card_to_use(cards):
    """
    Calcula la mejor tarjeta comparando qué tan lejos está el próximo corte.
    La mejor es la que acaba de cortar (tienes ~50 días para pagar).
    """
    if not cards:
        return None
    
    today = date.today()
    best_card = None
    max_days_until_payment = -1

    for card in cards:
        # Calcular fecha de próximo corte
        # Si el día de corte ya pasó este mes, el próximo es el siguiente mes
        try:
            current_month_closing = date(today.year, today.month, card.closing_day)
        except ValueError:
            # Manejo para meses con menos de 31 días
            last_day = (date(today.year, today.month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            current_month_closing = last_day

        if today <= current_month_closing:
            next_closing = current_month_closing
        else:
            # Próximo mes
            next_month = today.month + 1 if today.month < 12 else 1
            next_year = today.year if today.month < 12 else today.year + 1
            next_closing = date(next_year, next_month, card.closing_day)

        # Los días de financiamiento son aproximadamente (Días al corte + Días de gracia)
        # Aquí simplificamos buscando la que tenga el corte más lejano desde hoy
        days_until_closing = (next_closing - today).days
        
        if days_until_closing > max_days_until_payment:
            max_days_until_payment = days_until_closing
            best_card = card
            
    return best_card