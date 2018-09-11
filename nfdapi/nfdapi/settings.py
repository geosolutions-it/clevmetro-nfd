"""
Django settings for nfdapi project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/ref/settings/

"""

import datetime
import logging
import os

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _
import django_auth_ldap.config as ldap_config
import dj_database_url
import ldap


def get_environment_variable(var_name, default_value=None):
    value = os.getenv(var_name)
    if value is None:
        if default_value is None:
            error_msg = "Set the {0} environment variable".format(var_name)
            raise ImproperlyConfigured(error_msg)
        else:
            value = default_value
    return value


def get_boolean_env_value(environment_value, default_value=None):
    raw_value = get_environment_variable(
        environment_value,
        default_value=default_value
    )
    return True if raw_value.lower() in ("true", "1") else False


def get_list_env_value(environment_value, separator=":", default_value=None):
    raw_value = get_environment_variable(
        environment_value,
        default_value=default_value
    )
    return [item for item in raw_value.split(separator) if item != ""]


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MEDIA_ROOT = get_environment_variable(
    "DJANGO_MEDIA_ROOT",
    default_value=os.path.join(
        os.path.dirname(BASE_DIR),
        "media"
    )
)
MEDIA_URL = get_environment_variable(
    "DJANGO_MEDIA_URL",
    default_value='/media/'
)
STATIC_ROOT = get_environment_variable(
    "DJANGO_STATIC_ROOT",
    default_value=os.path.join(
        os.path.dirname(BASE_DIR),
        "static_root"
    )
)
STATIC_URL = get_environment_variable(
    "DJANGO_STATIC_URL",
    default_value='/nfdapi-static/'
)

APP_NAME = "nfdapi/"

SECRET_KEY = get_environment_variable("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_boolean_env_value("DJANGO_DEBUG", "false")

ALLOWED_HOSTS = get_list_env_value(
    "DJANGO_ALLOWED_HOSTS", separator=" ", default_value="*")

AUTH_USER_MODEL = 'nfdusers.user'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_filters',
    'reversion',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework.authtoken',
    'rest_auth',
    'nfdcore',
    'nfdusers',
    'nfdrenderers',
    'easy_pdf'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nfdapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nfdapi.wsgi.application'

DATABASES = {
    'default': dj_database_url.parse(
        get_environment_variable(
            'DJANGO_DATABASE_URL',
            default_value='sqlite:///{}'.format(
                os.path.join(BASE_DIR, 'db.sqlite3')
            )
        )
    ),
    'itis': dj_database_url.parse(
        get_environment_variable(
            'ITIS_DATABASE_URL'
        )
    )
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # it's very important to set first the TokenAuthentication because otherwise
        # the mobile apps fail to authenticate
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'nfdrenderers.xlsx.XlsxRenderer',
        'nfdrenderers.csv.CsvRenderer',
        'nfdrenderers.shp.ShpRenderer',
    )
}


JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'nfdcore.jwtutils.jwt_response_payload_handler',
    'JWT_ALLOW_REFRESH': True,
    #'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    #'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7)
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=10),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(hours=10),
    #'JWT_AUTH_COOKIE': 'nfdjwtauth'
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
"""
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
"""

AUTH_PASSWORD_VALIDATORS = []  # using AD/LDAP passwords validation rules

# Configuration for OpenLDAP
AUTH_LDAP_SERVER_URI = get_environment_variable("LDAP_HOST")
AUTH_LDAP_BIND_DN = get_environment_variable("LDAP_BIND_DN")
AUTH_LDAP_BIND_PASSWORD = get_environment_variable("LDAP_BIND_PASSWORD")
AUTH_LDAP_USER_SEARCH = ldap_config.LDAPSearch(
    get_environment_variable("LDAP_USER_SEARCH_DN"),
    ldap.SCOPE_SUBTREE,
    "(cn=%(user)s)"
)
AUTH_LDAP_GROUP_SEARCH = ldap_config.LDAPSearch(
    get_environment_variable("LDAP_GROUP_SEARCH_DN"),
    ldap.SCOPE_SUBTREE
)
AUTH_LDAP_GROUP_TYPE = ldap_config.NestedGroupOfNamesType()

AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300
AUTH_LDAP_MIRROR_GROUPS = True


def _build_ldap_group_dn(env_var_name, default,
                         suffix=AUTH_LDAP_GROUP_SEARCH.base_dn):
    cn = get_environment_variable(env_var_name, default_value=default)
    return ",".join((
        "cn={}".format(cn),
        suffix
    ))


AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_staff": _build_ldap_group_dn("LDAP_STAFF_CN", "nfdadmins"),
    "is_superuser": _build_ldap_group_dn("LDAP_ADMIN_CN", "nfdadmins"),
    "is_plant_writer": _build_ldap_group_dn(
        "LDAP_PLANT_WRITER_CN", "plant_writer"),
    "is_plant_publisher": _build_ldap_group_dn(
        "LDAP_PLANT_PUBLISHER_CN", "plant_publisher"),
    "is_animal_writer": _build_ldap_group_dn(
        "LDAP_ANIMAL_WRITER_CN", "animal_writer"),
    "is_animal_publisher": _build_ldap_group_dn(
        "LDAP_ANIMAL_PUBLISHER_CN", "animal_publisher"),
    "is_slimemold_writer": _build_ldap_group_dn(
        "LDAP_SLIMEMOLD_WRITER_CN", "slimemold_writer"),
    "is_slimemold_publisher": _build_ldap_group_dn(
        "LDAP_SLIMEMOLD_PUBLISHER_CN", "slimemold_publisher"),
    "is_fungus_writer": _build_ldap_group_dn(
        "LDAP_FUNGUS_WRITER_CN", "fungus_writer"),
    "is_fungus_publisher": _build_ldap_group_dn(
        "LDAP_FUNGUS_PUBLISHER_CN", "fungus_publisher"),
    "is_naturalarea_writer": _build_ldap_group_dn(
        "LDAP_NATURALAREA_WRITER_CN", "naturalarea_writer"),
    "is_naturalarea_publisher": _build_ldap_group_dn(
        "LDAP_NATURALAREA_PUBLISHER_CN", "naturalarea_publisher"),
}

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "cn",
    "last_name": "sn",
    "email": "mail"
}

# Configuration for Active Directory
# AUTH_LDAP_BIND_DN = "cn=Bind_User,ou=Users,dc=nfd,dc=geo-solutions,dc=it"
# AUTH_LDAP_BIND_PASSWORD = "kwNw8iqzr9p"
# AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Users,dc=nfd,dc=geo-solutions,dc=it",
#     ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
#
#
# AUTH_LDAP_GROUP_SEARCH = ldap_config.LDAPSearch(
#     "ou=Groups,dc=nfd,dc=geo-solutions,dc=it",
#     ldap.SCOPE_SUBTREE,
#     "(objectClass=group)")
# )
# AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
#
# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#     "is_staff": "cn=nfdadmins,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_superuser": "cn=nfdadmins,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_plant_writer": "cn=plant_writer,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_plant_publisher": "cn=plant_publisher,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_animal_writer": "cn=animal_writer,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_animal_publisher": "cn=animal_publisher,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_slimemold_writer": "cn=slimemold_writer,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_slimemold_publisher": "cn=slimemold_publisher,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_fungus_writer": "cn=fungus_writer,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_fungus_publisher": "cn=fungus_publisher,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_naturalarea_writer": "cn=naturalarea_writer,ou=groups,dc=nfd,dc=geo-solutions,dc=it",
#     "is_naturalarea_publisher": "cn=naturalarea_publisher,ou=groups,dc=nfd,dc=geo-solutions,dc=it"
# }
#
# AUTH_LDAP_USER_ATTR_MAP = {
#     "first_name": "givenName",
#     "last_name": "sn",
#     "email": "mail"
# }



#AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=nfdusers,dc=nfd,dc=geo-solutions,dc=it"
#AUTH_LDAP_START_TLS = True

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGES = [
  ('en', _('English'))
]
LOCALE_PATHS = [
    BASE_DIR + '/nfdcore/locale',
    BASE_DIR + '/locale',
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
#         },
#         'django_auth_ldap': {
#             'handlers': ['console'],
#             'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
#         },
#     },
# }
#
# AUTH_LDAP_CONNECTION_OPTIONS = {
#     ldap.OPT_DEBUG_LEVEL: 1,
#     ldap.OPT_REFERRALS: 0,
# }

NFDCORE_FORM_DEFINITIONS = {
    "common": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "common-pages.yml"),
    "ln": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "land-animal-forms.yml"),
    "st": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "stream-animal-forms.yml"),
    "lk": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "pond-lake-animal-forms.yml"),
    "we": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "wetland-animal-forms.yml"),
    "sl": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "slimemold-forms.yml"),
    "co": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "conifer-plant-forms.yml"),
    "fe": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "fern-plant-forms.yml"),
    "fl": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "flowering-plant-forms.yml"),
    "mo": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "moss-plant-forms.yml"),
    "fu": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "fungus-forms.yml"),
    "na": os.path.join(
        BASE_DIR, "nfdcore", "form_definitions", "natural-area-forms.yml"),
}

