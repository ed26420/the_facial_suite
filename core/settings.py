import os
from pathlib import Path
import dj_database_url
import requests
from dotenv import load_dotenv

# 1. Base Directory & Environment Variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env', override=True)

# 2. Security & Hosting Settings (Zero Fallbacks)

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.environ['SECRET_KEY']



ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')
try:
    token_url = 'http://169.254.169.254/latest/api/token'
    token_headers = {'X-aws-ec2-metadata-token-ttl-seconds': '3600'}
    token = requests.put(token_url, headers=token_headers, timeout=1).text

    ip_url = 'http://169.254.169.254/latest/meta-data/local-ipv4'
    ip_headers = {'X-aws-ec2-metadata-token': token}
    ec2_private_ip = requests.get(ip_url, headers=ip_headers, timeout=1).text
    
    if ec2_private_ip:
        ALLOWED_HOSTS.append(ec2_private_ip)
except requests.exceptions.RequestException:
    pass

CSRF_TRUSTED_ORIGINS = [
    'https://thefacialsuite.com',
    'https://www.thefacialsuite.com',
    'https://*.elasticbeanstalk.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 3. Application Definition
INSTALLED_APPS = [
    "pages",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'ckeditor',
    'storages',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'pages.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pages.context_processors.menu_categories",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# 4. Database Setup (Strictly AWS RDS - No SQLite Fallback)
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600
    )
}

# 5. Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 6. Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# 7. Static & Media Storage Configuration (Strictly AWS S3)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}



AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = os.getenv('AWS_REGION_NAME', 'eu-north-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None

STORAGES["default"] = {
    "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
}
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'


# 8. Third-Party Services (Zero Fallbacks)
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')



EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

SITE_URL = os.environ['SITE_URL']

LOGIN_URL = 'login'

import os

MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False').lower() == 'true'