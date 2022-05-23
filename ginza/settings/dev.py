import os
from datetime import datetime
import environ
from .base import *

now = datetime.now()
str_now = now.strftime('%y%m%d')

env = environ.Env()
BASE_DIR = os.path.abspath("/home/ec2-user")

ALLOWED_HOSTS = [
    '*'
]

# Take environment variables from .env file
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# Database
DB_NAME = env.str('DB_NAME')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.str('DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'ATOMIC_REQUESTS': True,
    }
}

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')
REDIS_DB = env.str('REDIS_DB')
REDIS_URL = 'redis://{}:{}/{}'.format(REDIS_HOST, REDIS_PORT, REDIS_DB)

# connect with Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

LOGGING_DIRECTORY = env.str('LOGGING_DIRECTORY')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'encoding': 'utf-8',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIRECTORY + '/ginza.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'api': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}


SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False
}

KAKAO_REST_API_KEY = env.str('KAKAO_REST_API_KEY')
KAKAO_REDIRECT_URI = env.str('KAKAO_REDIRECT_URI')
KAKAO_SECRET_KEY = env.str('KAKAO_SECRET_KEY')