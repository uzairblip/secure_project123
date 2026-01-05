import os
from pathlib import Path
import certifi
from dotenv import load_dotenv

# 1. BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. LOAD SECURE CREDENTIALS FROM .ENV [cite: 119]
load_dotenv(os.path.join(BASE_DIR, '.env'))

# ==============================================================================
# 🛡️ CORE SECURITY CONFIGURATION [cite: 66, 69]
# ==============================================================================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

# 🛠️ TEMPORARILY SET TO TRUE TO FIND THE LOGIN/CAPTCHA BUG
# Note: Revert to False for final submission to hide system maps [cite: 107, 120]
DEBUG = False 

# 🛡️ Required for validation; added '*' for easier local debugging [cite: 66]
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*']

# ==============================================================================
# 📦 APPLICATION DEFINITION
# ==============================================================================
INSTALLED_APPS = [
    'inventory',
    'captcha',                  # 🛡️ Anti-Automation / Bot Protection [cite: 75]
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',     # 🛡️ CSRF Protection [cite: 101, 185]
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # 🛡️ Location of custom 403/404.html 
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
# 💾 DATABASE & CACHING (BRUTE-FORCE PROTECTION) [cite: 125]
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3', # 🛡️ Uses ORM for SQLi prevention [cite: 96, 179]
    }
}

# 🛡️ Cache used for the 3-strike login lockout policy [cite: 125]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'login_lockout_cache',
    }
}

# ==============================================================================
# 🔐 AUTHENTICATION & REDIRECTION [cite: 98]
# ==============================================================================
LOGIN_URL = '/inventory/login/'
LOGIN_REDIRECT_URL = '/inventory/'
LOGOUT_REDIRECT_URL = '/inventory/login/'

# 🛡️ Strong password rules enforced [cite: 99]
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
# 🛡️ BROWSER SECURITY HEADERS (OWASP HARDENING) [cite: 102]
# ==============================================================================
X_FRAME_OPTIONS = 'DENY'            # 🛡️ Anti-Clickjacking [cite: 103]
SECURE_CONTENT_TYPE_NOSNIFF = True  # 🛡️ Prevent MIME-sniffing [cite: 102, 114]
SECURE_BROWSER_XSS_FILTER = True    # 🛡️ XSS Protection [cite: 132, 134]

# 🛡️ Secure Session Cookies [cite: 102]
SESSION_COOKIE_HTTPONLY = True   
CSRF_COOKIE_HTTPONLY = True      
SESSION_COOKIE_AGE = 600         # 🛡️ 10-minute timeout [cite: 100]
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ==============================================================================
# 📧 EMAIL CONFIGURATION (SECURE 2FA) [cite: 109, 112]
# ==============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_SSL_CAFILE = certifi.where() 

# ==============================================================================
# 📁 STATIC & MEDIA FILES (FILE UPLOAD SECURITY) [cite: 113]
# ==============================================================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles' # 🛡️ MANDATORY destination for collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'         # 🛡️ Stored outside web root [cite: 116]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# LOCAL DEVELOPMENT (SSL OFF FOR LOCALHOST)
# ==============================================================================
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'http://localhost:8000']