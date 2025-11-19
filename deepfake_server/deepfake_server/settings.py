from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+49$%9(l5eg5_c0w27c#a+k!te$hrp+y(v4de!b9nborw630if'
DEBUG = False
ALLOWED_HOSTS = ["*"]

# --------------------
# Installed apps
# --------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
]

# --------------------
# Middleware (CORS must be first)
# --------------------
MIDDLEWARE = [
    "deepfake_server.middleware.ForceCorsMiddleware",  # custom middleware to force CORS
    "corsheaders.middleware.CorsMiddleware",           # corsheaders
    "django.middleware.common.CommonMiddleware",      # must come after CORS
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------
# CORS Settings
# --------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://deepfake-detection-romo.onrender.com",
    "https://deep-fake-detection-peach.vercel.app",
    "http://localhost:5173"
]
CSRF_COOKIE_SECURE = False  # local testing

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --------------------
# URLs & Templates
# --------------------
ROOT_URLCONF = 'deepfake_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deepfake_server.wsgi.application'

# --------------------
# Database
# --------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------
# Localization
# --------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# --------------------
# Static Files
# --------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
