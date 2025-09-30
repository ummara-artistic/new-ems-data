import os
from pathlib import Path
import dj_database_url  # pip install dj-database-url psycopg2-binary
from urllib.parse import quote_plus
import socket

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------- Secret & Debug --------------------
SECRET_KEY = 'django-insecure-dev-key'
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.vercel.app'
]

# -------------------- Supabase Postgres --------------------
# URL-encode your password
DB_PASSWORD = quote_plus('orchard12@')  # replace with actual password

# Resolve host to IPv4
SUPABASE_HOST_IPV4 = socket.gethostbyname('db.agtzxtiqsieldeqwvilh.supabase.co')

# Connection pooling (recommended for Vercel / serverless)
DATABASE_URL = f"postgresql://postgres:{DB_PASSWORD}@{SUPABASE_HOST_IPV4}:6543/postgres?sslmode=require&pgbouncer=true"

# Direct connection (for management commands / migrations)
DIRECT_URL = f"postgresql://postgres:{DB_PASSWORD}@{SUPABASE_HOST_IPV4}:5432/postgres?sslmode=require"

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True),
    "direct": dj_database_url.parse(DIRECT_URL, conn_max_age=0, ssl_require=True),
}

# -------------------- Static & Media --------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------- Auth --------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# -------------------- Localization --------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
