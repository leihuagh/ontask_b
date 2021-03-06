"""
Django settings for ontask project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from os.path import dirname, join, exists

import environ
import json
from celery.schedules import crontab
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants

# import ldap
# from django_auth_ldap.config import (
#     LDAPSearch,
#     GroupOfNamesType,
#     LDAPGroupQuery
# )

# Use 12factor inspired environment variables or from a file and define defaults
env = environ.Env(
    DEBUG=(bool, False),
    SHOW_HOME_FOOTER_IMAGE=(bool, True),
    LTI_OAUTH_CREDENTIALS=(dict, {})
)

# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file_name = os.environ.get('ENV_FILENAME', 'local.env')
env_file = join(dirname(__file__), env_file_name)
if exists(env_file):
    print('Loading environment file {0}'.format(env_file_name))
    environ.Env.read_env(str(env_file))

# Read various variables from the environment
BASE_URL = env('BASE_URL', default='')
DOMAIN_NAME = env('DOMAIN_NAME')
DEBUG = env('DEBUG')
SHOW_HOME_FOOTER_IMAGE = env('SHOW_HOME_FOOTER_IMAGE')

# Build paths inside the project like this: join(BASE_DIR(), "directory")
BASE_DIR = environ.Path(__file__) - 3
STATICFILES_DIRS = [join(BASE_DIR(), 'static')]
MEDIA_ROOT = join(BASE_DIR(), 'media')
MEDIA_URL = BASE_URL + "/media/"
ONTASK_HELP_URL = "html/index.html"

# Project root folder (needed somewhere in Django
PROJECT_PATH = BASE_DIR()

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR(), 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'ontask.context_processors.conf_to_context',
            ],
            'libraries': {
                'ontask_tags': 'ontask.templatetags.ontask_tags',
                'vis_include': 'visualizations.templatetags.vis_include',
            }
        },
    },
]

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    'django_extensions',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_celery_beat',
    'django_celery_results',
    'bootstrap_datepicker_plus',

    'authtools',
    'crispy_forms',
    'easy_thumbnails',
    'widget_tweaks',
    'formtools',
    'siteprefs',
    'django_tables2',
    'import_export',
    'rest_framework',
    'rest_framework.authtoken',
    'django_summernote',
    'jquery',
    'django_auth_lti',

    'accounts',
    'core.apps.CoreConfig',
    'profiles.apps.ProfileConfig',
    'workflow.apps.WorkflowConfig',
    'dataops.apps.DataopsConfig',
    'table.apps.TableConfig',
    'action.apps.ActionConfig',
    'logs.apps.LogsConfig',
    'scheduler.apps.SchedulerConfig',
    'ontask_oauth.apps.OnTaskOauthConfig',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_auth_lti.middleware_patched.MultiLTILaunchAuthMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

LOCALE_PATHS = [join(PROJECT_PATH, 'locale')]

AUTHENTICATION_BACKENDS = [
    'django_auth_lti.backends.LTIAuthBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
    # 'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env('REDIS_URL'),
        "TIMEOUT": 1800,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "KEY_PREFIX": "ontask"
        },
    }
}

# Cache time to live is 15 minutes
CACHE_TTL = 60 * 30
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # set just 30 mins
SESSION_SAVE_EVERY_REQUEST = True  # Needed to make sure timeout above works
X_FRAME_OPTIONS = 'SAMEORIGIN'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    # ),
    # 'DEFAULT_PARSER_CLASSES': (
    #     'rest_framework.parsers.JSONParser',
    # )
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/minute',
        'user': '1000/minute'
    }
}

ROOT_URLCONF = 'ontask.urls'

WSGI_APPLICATION = 'ontask.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db(),
}

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_URL = BASE_URL + '/static/'

# Crispy Form Theme - Bootstrap 4
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# For Bootstrap 3, change error alert to 'danger'
MESSAGE_STORE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

################################################################################
#
# Authentication Settings
#
################################################################################
AUTH_USER_MODEL = 'authtools.User'
LOGIN_REDIRECT_URL = reverse_lazy("home")
LOGIN_URL = reverse_lazy("accounts:login")

THUMBNAIL_EXTENSION = 'png'  # Or any extn for your thumbnails

IMPORT_EXPORT_USE_TRANSACTIONS = True

SITE_ID = 1

################################################################################
#
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
#
################################################################################
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', _('English')),
    ('es-es', _('Spanish')),
    ('zh-cn', _('Chinese')),
    ('fi', _('Finnish')),
)

################################################################################
#
# SUMMERNOTE CONFIGURATION
#
################################################################################
SUMMERNOTE_THEME = 'bs4'
SUMMERNOTE_CONFIG = {
    'iframe': False,
    'summernote': {
        'width': '100%',
        'height': '400px',
        'disableDragAndDrop': True,
    },
    'css': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/base16-dark.min.css',
    ),
    'css_for_inplace': (
        '//cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/base16-dark.min.css',
    ),
    'codemirror': {
        'theme': 'base16-dark',
        'mode': 'htmlmixed',
        'lineNumbers': True,
        'lineWrapping': True,
    },
    # Disable attachment feature.
    'disable_attachment': False,
    'lazy': True,
}

################################################################################
#
# DATA UPLOAD FILES
#
################################################################################
DATAOPS_CONTENT_TYPES = '["text/csv", "application/json", "application/gzip", "application/x-gzip", "application/vnd.ms-excel"]'
DATAOPS_MAX_UPLOAD_SIZE = 209715200  # 200 MB

# Raise because default of 1000 is too short
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

################################################################################
#
# Email sever configuration
#
################################################################################
EMAIL_HOST = env.str('EMAIL_HOST', default='')
EMAIL_PORT = env.str('EMAIL_PORT', default='')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = env.bool('EMAIL_HOST_TLS', default=False)
EMAIL_USE_SSL = env.bool('EMAIL_HOST_SSL', default=False)

# Number of emails to send out in a burst (before pausing)
EMAIL_BURST = env.int('EMAIL_BURST', default=0)
# Pause between bursts (in seconds)
EMAIL_BURST_PAUSE = env.int('EMAIL_BURST_PAUSE', default=0)

# Additional email related variables
EMAIL_ACTION_NOTIFICATION_TEMPLATE = """
<html>
<head/>
<body>
<p>Dear {{ user.name }}</p>

<p>This message is to inform you that on {{ email_sent_datetime }}
{{ num_messages }} email{% if num_messages > 1 %}s{% endif %} were sent
resulting from the execution of the action with name "{{ action.name }}".</p>

{% if filter_present %}
<p>The action had a filter that reduced the number of messages from
{{ num_rows }} to {{ num_selected }}.</p>
{% else %}
<p>All the data rows stored in the workflow table were used.</p>
{% endif %}

Regards.
The OnTask Support Team
</body></html>"""

EMAIL_ACTION_NOTIFICATION_SUBJECT = _("OnTask: Action executed")
EMAIL_ACTION_NOTIFICATION_SENDER = \
    env.str('EMAIL_ACTION_NOTIFICATION_SENDER', default='')
EMAIL_ACTION_PIXEL = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGP6zwAAAgcBApocMXEAAAAASUVORK5CYII='

################################################################################
#
# Log configuration
#
################################################################################
LOGS_MAX_LIST_SIZE = 200
SHORT_DATETIME_FORMAT = 'r'

################################################################################
#
# Execute JSON transfer: If False, the personalized JSON and Canvas email
# do not send the data but instead log the content of the JSON objects through
# the logger
#
################################################################################
EXECUTE_ACTION_JSON_TRANSFER = env.bool('EXECUTE_ACTION_JSON_TRANSFER',
                                        default=False)

################################################################################
#
# Scheduler configuration
#
################################################################################
SCHEDULER_MINUTE_STEP = 15

################################################################################
#
# CELERY parameters
#
################################################################################
CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = env('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {
    'ontask_scheduler': {
        'task': 'ontask.tasks.execute_scheduled_actions',
        'schedule': crontab(minute='*/{0}'.format(SCHEDULER_MINUTE_STEP)),
        'args': (DEBUG,)
    }
}

#
# LDAP AUTHENTICATION
#
# Variables taken from local.env
# AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI')
# AUTH_LDAP_BIND_PASSWORD = env('AUTH_LDAP_BIND_PASSWORD')

# Additional configuration variables (read django-auth-ldap documentation)
# AUTH_LDAP_CONNECTION_OPTIONS = {
# }
# AUTH_LDAP_BIND_DN = "cn=admin,dc=bogus,dc=com"
# AUTH_LDAP_USER_SEARCH = LDAPSearch(
#     "ou=people,dc=bogus,dc=com",
#     ldap.SCOPE_SUBTREE,
#     "(uid=%(user)s)")
# AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,dc=bogus,dc=com"
# AUTH_LDAP_START_TLS = True
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,dc=example,dc=com",
#     ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
# )
# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
# AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=groups,dc=example,dc=com"
# AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=groups,dc=example,dc=com"
# AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn"}
# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_active": "cn=active,ou=groups,dc=example,dc=com",
#     "is_staff": (
#         LDAPGroupQuery("cn=staff,ou=groups,dc=example,dc=com") |
#         LDAPGroupQuery("cn=admin,ou=groups,dc=example,dc=com")
#     ),
#     "is_superuser": "cn=superuser,ou=groups,dc=example,dc=com"
# }
# AUTH_LDAP_ALWAYS_UPDATE_USER = True
# AUTH_LDAP_FIND_GROUP_PERMS = True
# AUTH_LDAP_CACHE_GROUPS = True
# AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300


#
# LTI Authentication
#
LTI_OAUTH_CREDENTIALS = env('LTI_OAUTH_CREDENTIALS')

################################################################################
#
# CANVAS API ENTRY POINTS
#
################################################################################
CANVAS_INFO_DICT = json.loads(env.str('CANVAS_INFO_DICT', default='{}'))
# The string in the .env file must be a single line JSON encoding of a
# dictionary with the following elements:
#   "Server name or domain descriptor (shown to the user": {
#      domain_port: VALUE,
#      client_id: VALUE,
#      client_secret: VALUE ,
#      authorize_url: VALUE (format {0} for domain_port),
#      access_token_url: VALUE (format {0} for domain_port),
#      conversation_URL: VALUE (format {0} for domain_port),
#      aux_params: DICT with additional parameters)
#    }
#  For example:
#
#  CANVAS_INFO_DICT={"Server one": {"domain_port": "yourcanvasdomain.edu", "client_id": "10000000000001", "client_secret": "YZnGjbkopt9MpSq2fujUOgbeVZ8NdkdCeGF2ufhWZdBKAZvNCuuTOWXHotsWMu6X", "authorize_url": "http://{0}/login/oauth2/auth", "access_token_url": "http://{0}/login/oauth2/token", "conversation_url": "http://{0}/api/v1/conversations", "aux_params": {"burst": 10, "pause": 5}}}

# Number of seconds left in the token validity to refresh
CANVAS_TOKEN_EXPIRY_SLACK = env.int('CANVAS_TOKEN_EXPIRY_SLACK', default=600)
