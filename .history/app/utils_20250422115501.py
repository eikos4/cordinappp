from app import db
from app.models import Notification

def send_notification(recipient_id, message):
    notification = Notification(
        recipient_id=recipient_id,
        message=message
    )
    db.session.add(notification)
    db.session.commit()




