from datetime import datetime
from app import db
from app.models import Notification

def send_notification(recipient_id, message):
    notification = Notification(
        recipient_id=recipient_id,
        message=message
    )
    db.session.add(notification)
    db.session.commit()

def build_timeline(registros):
    timeline = []
    prev_time = None

    for log in registros:
        delta = 0
        if prev_time:
            try:
                delta = (log.timestamp.date() - prev_time.date()).days
            except Exception as e:
                print("Error al calcular diferencia de días:", e)
                delta = 0
        prev_time = log.timestamp  # mantener como datetime completo
        timeline.append({
            'log': log,
            'margin_top': int(delta * 20)  # espaciado proporcional
        })
    return timeline
