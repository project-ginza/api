from .base import *
import environ, os

env = environ.Env()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Take environment variables from .env file
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {'default': env.db('DATABASE_URL')}