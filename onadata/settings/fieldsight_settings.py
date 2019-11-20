import os
from onadata.settings.kc_environ import *
from onadata.settings.common import REST_FRAMEWORK

KOBOCAT_URL = os.environ.get('KOBOCAT_URL', 'http://localhost:8001')

XML_VERSION_MAX_ITER = 6
KPI_DEFAULT_FORM1_STRING = "amzrDJHu2d74f8KNdYTrEY"
ASSET_CONTENT_TYPE_ID = 21

KOBOCAT_INTERNAL_HOSTNAME = "localhost"
# ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'https')
# ENKETO_PROTOCOL = os.environ.get('ENKETO_PROTOCOL', 'http')
ENKETO_PROTOCOL = 'http'
ENKETO_API_ENDPOINT_SURVEYS = '/survey'

ENKETO_URL = os.environ.get('ENKETO_URL', 'http://localhost:8005')
ENKETO_PREVIEW_URL = ENKETO_URL + os.environ.get('ENKETO_API_ENDPOINT_PREVIEW', '/preview')

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SITE_URL = 'http://localhost:8001'
SITE_EMAIL = 'example.com'

KPI_ASSET_URL = 'http://localhost:8000/assets/'

KOBOCAT_URL = 'http://localhost:8001'

# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'localhost:8001',
    'http://localhost:8001',
    'localhost:8000',
    '127.0.0.1:8001',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8001',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('POSTGRES_DB','fieldsight'),
        'USER': os.environ.get('POSTGRES_USER', 'fieldsight'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'fieldsight'),
        'HOST': os.environ.get('POSTGRES_HOST','postgis'),
        'PORT': os.environ.get('POSTGRES_PORT','5432'),
    }
}

INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS += ['rest_framework_docs', 'social_django', 'onadata.apps.eventlog', 'fcm', #'channels',
                   'onadata.apps.fieldsight', 'onadata.apps.fsforms',  'onadata.apps.fv3',
                   'onadata.apps.geo', 'onadata.apps.remote_app', 'onadata.apps.staff', 'onadata.apps.subscriptions',
                   'onadata.apps.userrole', 'onadata.apps.users','linaro_django_pagination',  'webstack_django_sorting','debug_toolbar']


TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS)

TEMPLATE_CONTEXT_PROCESSORS +=[
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect',
    'onadata.apps.eventlog.context_processors.events',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)

MIDDLEWARE_CLASSES += ['linaro_django_pagination.middleware.PaginationMiddleware',
                       'onadata.apps.users.middleware.RoleMiddleware',
                       'debug_toolbar.middleware.DebugToolbarMiddleware',
                       'social_django.middleware.SocialAuthExceptionMiddleware',
                       ]


INTERNAL_IPS = '127.0.0.1'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
        "ROUTING": "onadata.apps.fieldsight.routing.channel_routing",
    },
}


AUTHENTICATION_BACKENDS += (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)

WEBSOCKET_URL = "ws://localhost"

WEBSOCKET_PORT = "8001"

#koboformbuilder
KPI_URL = 'http://localhost:8000/'
KPI_LOGOUT_URL = KPI_URL + 'accounts/logout/'

FCM_DEVICE_MODEL = 'fcm.Device'

FCM_APIKEY = os.environ.get('FCM_APIKEY')
FCM_MAX_RECIPIENTS = 1000

SERIALIZATION_MODULES = {
        "custom_geojson": "onadata.apps.fieldsight.serializers.GeoJSONSerializer",
}


SEND_ACTIVATION_EMAIL = True
ACCOUNT_ACTIVATION_DAYS = 30
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''


TIME_ZONE = 'Asia/Kathmandu'

REST_FRAMEWORK.update({'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated',]})

STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/users/create-profile/'
SOCIAL_AUTH_LOGIN_URL = '/accounts/login/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.user.get_username',
    'onadata.apps.users.pipeline.email_validate',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'onadata.apps.users.pipeline.create_role',
    'onadata.apps.users.pipeline.create_profile',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")

DEBUG = True

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
SESSION_COOKIE_NAME = 'my_cookie'
DEFAULT_DEPLOYMENT_BACKEND = 'localhost'
SESSION_COOKIE_DOMAIN = 'localhost'


BROKER_BACKEND = "redis"
CELERY_RESULT_BACKEND = "redis"  # telling Celery to report results to RabbitMQ

CELERY_BROKER_URL = 'redis://localhost:6379'
REDIS_HOST = "localhost"

FRONTEND_ENVIRONMENT_DEV_MODE = True

