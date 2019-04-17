from __future__ import absolute_import

import stripe
from celery import shared_task
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task(time_limit=120, soft_time_limit=120)
def email_after_updating_plan(user, stripe_customer):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    data = stripe.Charge.list(customer=stripe_customer)
    receipt_url = data[0]['receipt_url']

    mail_subject = 'Update Plan'
    message = render_to_string('subscriptions/update_plan_email.html', {
        'user': user,
        'receipt_url': receipt_url,
        'domain': settings.SITE_URL,
    })
    to_email = user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()