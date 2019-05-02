from datetime import datetime

from django.conf import settings
from django.db.models import Q
from fcm.utils import get_device_model

from onadata.apps.userrole.models import UserRole

noti = settings.MONGO_DB.notifications


def get_notifications_queryset(email, date=None):
    query = {'emails': email}
    if date:
        query = {"$and": [{"date": {"$gt": date}}, query]}
    qs = noti.find(query, {'message': 1, '_id': 0, 'date': 1})
    return [n for n in qs]


def save_notification(message, emails, date=None):
    if not date:
        date = datetime.now()
    clean_emails = [str(e) for e in emails]

    notification = {'date': date,
                    'message': message,
                    'emails': clean_emails}
    noti.insert(notification)


def notify_koboform_updated(xform):
    from onadata.apps.fsforms.models import FieldSightXF
    project_ids = FieldSightXF.objects.filter(xf=xform).values_list('project_id', flat=True).distinct().order_by()
    site_ids = FieldSightXF.objects.filter(xf=xform).values_list('site_id', flat=True).distinct().order_by()
    project_ids = [v for v in project_ids if v]
    site_ids = [v for v in site_ids if v]
    emails = UserRole.objects.filter(ended_at=None,
                                    group__name__in=["Site Supervisor", "Region Supervisor"]
                                     ).filter(
        Q(site__id__in=site_ids) | Q(site__project__id__in=project_ids)
                                    ).values_list('user__email', flat=True).distinct().order_by()
    Device = get_device_model()
    is_delete = False
    message = {'notify_type': 'Form',
               'is_delete': is_delete,
               'form_name': xform.title,
               'xfid': xform.id_string,
               'form_type': "", 'form_type_id':"",
               'status': "Form Updated",
               'site': {}}
    save_notification(message, emails)
    Device.objects.filter(name__in=emails).send_message(message)

