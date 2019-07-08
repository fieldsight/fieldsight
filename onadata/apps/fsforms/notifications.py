from datetime import datetime

from django.conf import settings
from django.db.models import Q
from fcm.utils import get_device_model

noti = settings.MONGO_DB.notifications


def get_notifications_queryset(email, date=None, previous_next_type=None):
    query = {'emails': email}
    if date:
        if previous_next_type in [1, "1"]:
            query = {"$and": [{"date": {"$lt": date}}, query]}
            qs = noti.find(query, {'message': 1, '_id': 0, 'date': 1}).sort("date", -1).limit(15)
        else:
            query = {"$and": [{"date": {"$gt": date}}, query]}
            qs = noti.find(query, {'message': 1, '_id': 0, 'date': 1}).sort("date", 1).limit(15)
        return [n for n in qs]
    return []


def save_notification(message, emails, date=None):
    if not date:
        date = datetime.now()
    clean_emails = [str(e) for e in emails]

    notification = {'date': date,
                    'message': message,
                    'emails': clean_emails}
    noti.insert(notification)

