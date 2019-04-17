from __future__ import absolute_import

import time
import stripe
from celery import shared_task
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task(time_limit=120, soft_time_limit=120)
def email_after_updating_plan(user, receipt_url, plan_name, submissions):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    mail_subject = 'Update Plan'
    message = render_to_string('subscriptions/update_plan_email.html', {
        'user': user,
        'submissions': submissions,
        'receipt_url': receipt_url,
        'plan_name': plan_name,
        'domain': settings.SITE_URL,
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()