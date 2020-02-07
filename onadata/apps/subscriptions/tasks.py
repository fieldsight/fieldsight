# from __future__ import absolute_import
#
# import dateutil
# import stripe
# import time
#
# from celery import shared_task, task
# from django.conf import settings
# from django.utils import timezone
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from django.contrib.auth.models import User
#
# from datetime import datetime, timedelta
#
# from .models import Subscription
#
#
# @shared_task()
# def email_after_updating_plan(user_id, receipt_url, sub_id, amount, template, mail_subject, brand):
#     time.sleep(10)
#     user = User.objects.get(id=user_id)
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     mail_subject = mail_subject
#     sub_obj = Subscription.objects.get(id=sub_id)
#     plan_name = sub_obj.package.get_plan_display()
#     submissions = sub_obj.package.submissions
#     period = sub_obj.package.period_type
#     period_type = sub_obj.package.get_period_type_display()
#     usage_submissions = sub_obj.organization.get_total_submissions()
#     ending_date = {
#         1: datetime.now() + dateutil.relativedelta.relativedelta(months=1),
#         2: datetime.now() + dateutil.relativedelta.relativedelta(months=12)
#     }
#     start_date = datetime.now().strftime('%d-%m-%Y')
#     end_date = ending_date[period].strftime('%d-%m-%Y')
#     message = render_to_string(template, {
#         'user': user,
#         'submissions': submissions,
#         'receipt_url': receipt_url,
#         'plan_name': plan_name,
#         'start_date': start_date,
#         'end_date': end_date,
#         'period': period_type,
#         'amount': amount/100,
#         'domain': settings.SITE_URL,
#         'usage_submissions': usage_submissions,
#         'brand': brand
#     })
#     to_email = user.email
#     email = EmailMessage(
#         mail_subject, message, to=[to_email]
#     )
#     email.content_subtype = "html"
#
#     email.send()
#
#
# @shared_task()
# def notification_before_one_week_renewal(user_id):
#     user = User.objects.get(id=user_id)
#     mail_subject = 'Notification'
#     message = render_to_string('subscriptions/notification_before_renewal.html', {
#         'user': user,
#         'time': "week"
#
#     })
#     to_email = user.email
#     email = EmailMessage(
#         mail_subject, message, to=[to_email]
#     )
#     email.content_subtype = "html"
#     email.send()
#
#
# @shared_task()
# def notification_before_renewal(user_id):
#     """
#     Send email in week and month before renewal of annual plan.
#     Args:
#         user_id: user object
#
#     Returns:
#
#     """
#     user = User.objects.get(id=user_id)
#     mail_subject = 'Notification'
#     message = render_to_string('subscriptions/notification_before_renewal.html', {
#         'user': user,
#         'time': "month"
#     })
#     to_email = user.email
#     email = EmailMessage(
#         mail_subject, message, to=[to_email]
#     )
#     email.content_subtype = "html"
#     email.send()
#
#     week_before_renew = timezone.now() + timedelta(days=23)
#     notification_before_one_week_renewal.apply_async(args=[user_id], eta=week_before_renew)
#
