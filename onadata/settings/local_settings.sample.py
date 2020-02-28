import os

from celery.schedules import crontab

from onadata.settings.kc_environ import *
CORS_ORIGIN_ALLOW_ALL = True
KOBOCAT_URL = os.environ.get('KOBOCAT_URL')

KPI_DEFAULT_FORM1_STRING = "a5AZfY3qGtfkawaTnVzgtV"
KOBOCAT_INTERNAL_HOSTNAME = os.environ.get("KOBOCAT_INTERNAL_HOSTNAME", "kobo")
ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'https')

ENKETO_API_ENDPOINT_SURVEYS = '/survey'

ENKETO_URL = os.environ.get('ENKETO_URL', 'https://enketo.naxa.com.np')
ENKETO_PREVIEW_URL = ENKETO_URL + os.environ.get('ENKETO_API_ENDPOINT_PREVIEW', '/preview')

XML_VERSION_MAX_ITER = 6
ASSET_CONTENT_TYPE_ID = 20
DATABASES = {
    'defauli1': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fieldapp',
        'USER': 'kobo',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    },
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('POSTGRES_DB', ''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', ''),
    }
}


INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS += ['rest_framework_docs', 'social_django', 'onadata.apps.eventlog', 'fcm', "debug_toolbar",
                   'onadata.apps.fieldsight', 'onadata.apps.fsforms', 'onadata.apps.reporting',
                   'onadata.apps.geo', 'onadata.apps.remote_app', 'onadata.apps.staff', 'onadata.apps.subscriptions',
                   'onadata.apps.userrole', 'onadata.apps.users',
                   'linaro_django_pagination', 'webstack_django_sorting', 'onadata.apps.fv3']


MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)

MIDDLEWARE_CLASSES += ['linaro_django_pagination.middleware.PaginationMiddleware',
                       'onadata.apps.users.middleware.RoleMiddleware', 'debug_toolbar.middleware.DebugToolbarMiddleware']

AUTHENTICATION_BACKENDS += (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY","google auth2 key")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "google auth2 auth SECRET_KEY")

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/users/create-profile/'
SOCIAL_AUTH_LOGIN_URL = '/accounts/login/'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.'
    '',
    'onadata.apps.users.pipeline.email_validate',
    'onadata.apps.users.pipeline.create_role',
    'onadata.apps.users.pipeline.create_profile',

)

KPI_URL = os.environ.get('KPI_URL', 'https://kpi.naxa.com.np/')
KPI_ASSET_URL = os.environ.get('KPI_ASSET_URL')
#KPI_LOGOUT_URL = KPI_URL + 'accounts/logout/'
FCM_APIKEY = os.environ.get('FCM_APIKEY')

FCM_MAX_RECIPIENTS = 1000

SERIALIZATION_MODULES = {
        "custom_geojson": "onadata.apps.fieldsight.serializers.GeoJSONSerializer",
        "full_detail_geojson": "onadata.apps.fieldsight.serializers.FullDetailGeoJSONSerializer",
}
SEND_ACTIVATION_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 30
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND','django.core.mail.backends.smtp.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'test.fieldsight@gmail.com')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL','test.fieldsight@gmail.com')
EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '587')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'test@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'password')

USE_TZ = True
TIME_ZONE = os.environ.get('TIME_ZONE', 'Asia/Kathmandu')


from onadata.settings.common import REST_FRAMEWORK


REST_FRAMEWORK.update({'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated',]})
FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

#INSTALLED_APPS += ['debug_toolbar']

#DEBUG_TOOLBAR_CONFIG = {
#     'INTERCEPT_REDIRECTS': True
#}
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME','testapp_kobo_cookie')
SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN','.naxa.com.np')
#CSRF_COOKIE_DOMAIN = '.fieldsight.org'
DEFAULT_DEPLOYMENT_BACKEND = 'kobocat'
ADMINS = [('Amulya', 'awemulya@gmail.com'), ('saroj', 'raesaroj16@gmail.com'), ('santosh', 'skhatri.np@gmail.com')]

#Celery configuration
CELERY_BROKER_BACKEND = os.environ.get('CELERY_BROKER_BACKEND', "redis")
CELERY_TASK_ALWAYS_EAGER = os.environ.get('CELERY_TASK_ALWAYS_EAGER', False)
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://redis_main:6379/1')

# telling Celery to report results to This broker
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis_main:6379/1')


DEBUG = False
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')

SITE_URL = os.environ.get('KOBOCAT_URL')
# MEDIA_URL = '%s/media/'%os.environ.get('KOBOCAT_URL')

#dont need this after library form feature.
DEFAULT_FORM_2 = {
    'id_string': 'a4MJ2XJ9LEogrkCd8CsHvq',
    'name': 'Daily Site Diary - Default Form',
    'type':'schedule '
}

DEFAULT_FORM_1 = {
    'id_string': 'afZDovStsU5i7bH4kWx5mD',
    'name': 'Health, Safety, Social and Environmental Inspection Report - Default Form',
    'type':'schedule '
}
DEFAULT_FORM_3 = {
    'id_string': 'abk38CVVcLzec98n8S7LQD',
    'name': 'Incident Report',
    'type':'general'
}

SITE_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',
    }
}
INTERNAL_IPS = ['127.0.0.1']

SERVICE_ACCOUNT_JSON = os.environ.get('SERVICE_ACCOUNT_JSON', 'service_account.json')
SERVICE_ACCOUNT_EMAIL = os.environ.get('SERVICE_ACCOUNT_EMAIL', '.iam.gserviceaccount.com')
REPORT_ACCOUNT_EMAIL = os.environ.get('REPORT_ACCOUNT_EMAIL', '@gmail.com')


#bucket media path given by google
MEDIA_LOCATION_URL = os.environ.get('MEDIA_LOCATION_URL', 'https://testbucket.gcloud.com/')


DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage')
GS_BUCKET_NAME = os.environ.get('GS_BUCKET_NAME', '')
GS_PROJECT_ID = os.environ.get('GS_PROJECT_ID', '')


# google storage
#https://django-storages.readthedocs.io/en/1.8/backends/gcloud.html
# get signed urls make secures not public
# GS_DEFAULT_ACL = 'publicRead'

#Dont need Expiry urls. django storage docs.

GS_EXPIRATION = os.environ.get('GS_EXPIRATION', 86400 * 24 * 365 * 100)

# Needed when behind load balancer with ssl offloading. an example value is: HTTP_X_FORWARDED_PROTO
SECURE_PROXY_SSL_HEADER_NAME = os.environ.get('SECURE_PROXY_SSL_HEADER_NAME', '')
if SECURE_PROXY_SSL_HEADER_NAME:
    SECURE_PROXY_SSL_HEADER = (SECURE_PROXY_SSL_HEADER_NAME, 'https')


CELERY_BEAT_SCHEDULE = {
    "update_sheet_in_drive": {
        "task": "onadata.apps.reporting.tasks.sync_report",
        "schedule": crontab(minute=30, hour=23),  # execute daily at 6pm
        'options': {'queue': 'beat'}

    }
}


#google drive id
PARENT_FOLDER_ID = os.environ.get('PARENT_FOLDER_ID', '****')