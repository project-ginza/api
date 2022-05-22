from .base import * # do not optimize

import os
from datetime import datetime

import environ

now = datetime.now()
str_now = now.strftime('%y%m%d')

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = ['*']

# Take environment variables from .env file
# environ.Env.read_env(
#     env_file=os.path.join(BASE_DIR, '.env')
# )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'just-test-secret-key'

# Database
# DB_NAME = env.str('DB_NAME')
# DB_USER = env.str('DB_USER')
# DB_PASSWORD = env.str('DB_PASSWORD')
# DB_HOST = env.str('DB_HOST')
# DB_PORT = env.str('DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
    }
}

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)

#connect with Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# LOGGING_DIRECTORY = env.str('LOGGING_DIRECTORY')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'formatters': {
#         'django.server': {
#             '()': 'django.utils.log.ServerFormatter',
#             'format': '[{server_time}] {message}',
#             'style': '{',
#         },
#         'standard': {
#             'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         },
#         'django.server': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'django.server',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'INFO',
#         },
#         'django.server': {
#             'handlers': ['django.server'],
#             'level': 'DEBUG',
#             'propagate': False,
#         },
#         'api': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False,
#         },
#     }
# }