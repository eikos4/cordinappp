from datetime import datetime
from app import db
from app.models import Notification, User

# Notificación individual
def crear_notificacion(user_id, mensaje):
    notificacion = Notification(recipient_id=user_id, message=mensaje)
    db.session.add(notificacion)
    db.session.commit()

# Notificar a todos los administradores
def notificar_admins(mensaje):
    from app.models import User
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        send_notification(admin.id, mensaje)

# Notificar a todos los líderes del proyecto
def notificar_lideres(mensaje, project):
    for pu in project.participants:
        if pu.user.role == 'leader':
            send_notification(pu.user.id, mensaje)

# Para notificaciones rápidas (opcional: usa esta si no necesitas rol check)
def send_notification(recipient_id, message):
    notification = Notification(
        recipient_id=recipient_id,
        message=message
    )
    db.session.add(notification)
    db.session.commit()

# Utilidad para construir línea de tiempo de bitácora
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
        prev_time = log.timestamp
        timeline.append({
            'log': log,
            'margin_top': int(delta * 20)
        })
    return timeline
