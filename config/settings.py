import os
from pathlib import Path
import certifi
from dotenv import load_dotenv

# 1. BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. LOAD SECURE CREDENTIALS FROM .ENV
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ==============================================================================
# 🛡️ CORE SECURITY CONFIGURATION
# ==============================================================================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

# 🛡️ Mandatory for production: DEBUG=False prevents URL pattern disclosure
DEBUG = False 

# 🛡️ Required when DEBUG is False to verify the host
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ==============================================================================
# 📦 APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    'inventory',
    'captcha',                  # 🛡️ Anti-Automation / Bot Protection
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 🛡️ Stays at top for header processing
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # 🛡️ Anti-Clickjacking
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # 🛡️ Django looks here for your 403/404.html
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

WSGI_APPLICATION = 'config.wsgi.application'

# ==============================================================================
# 💾 DATABASE & CACHING (BRUTE-FORCE PROTECTION)
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🛡️ Database-backed Cache used for the 3-strike lockout policy
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'login_lockout_cache',
    }
}

# ==============================================================================
# 🔐 AUTHENTICATION & REDIRECTION
# ==============================================================================
# 🛡️ Fixes the redirection loop to default "accounts/login/"
LOGIN_URL = '/inventory/login/'
LOGIN_REDIRECT_URL = '/inventory/'
LOGOUT_REDIRECT_URL = '/inventory/login/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# 🛡️ BROWSER SECURITY HEADERS (OWASP HARDENING)
# ==============================================================================
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_HTTPONLY = True   # 🛡️ Prevents JS from accessing session cookies
CSRF_COOKIE_HTTPONLY = True      # 🛡️ Prevents JS from accessing CSRF tokens
SESSION_COOKIE_AGE = 600         # 🛡️ Auto-logout after 10 minutes
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ==============================================================================
# 📧 EMAIL CONFIGURATION (SECURE 2FA)
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_SSL_CAFILE = certifi.where() 

# ==============================================================================
# 📁 STATIC & MEDIA FILES
# ==============================================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

# 🛡️ Mandatory for DEBUG=False to serve assets correctly
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# LOCAL DEVELOPMENT (SSL OFF FOR LOCALHOST)
# ==============================================================================
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']