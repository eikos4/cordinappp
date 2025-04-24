from app import db
from app.models import Notification

def send_notification(recipient_id, message):
    notification = Notification(
        recipient_id=recipient_id,
        message=message
    )
    db.session.add(notification)
    db.session.commit()



from datetime import datetime

# Calcular diferencia en días entre eventos
def build_timeline(registros):
    timeline = []
    prev_time = None

    for log in registros:
        delta = 0
        if prev_time:
            # Ambos convertidos explícitamente a date
            delta = (log.timestamp.date() - prev_time.date()).days
        prev_time = log.timestamp
        timeline.append({
            'log': log,
            'margin_top': int(delta * 20)  # 20px por día
        })
    return timeline

