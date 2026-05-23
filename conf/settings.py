import os
from pathlib import Path
from environs import Env

# Initialisation des variables d'environnement
env = Env()
env.read_env() # Lit un fichier .env s'il existe en local

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SÉCURITÉ : Clé secrète dynamique en prod, clé par défaut en local
SECRET_KEY = env.str('SECRET_KEY', default='django-insecure-oy6uxxie@7-w#)$9fkhtj15uac$_k2$xf1iflrr&x6e-e#2d(6')

# SÉCURITÉ : Doit être obligatoirement False en production
DEBUG = env.bool('DEBUG', default=True)

# Gestion des hôtes autorisés
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Essentiel pour la prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

# Configuration des Templates (Requis pour l'admin Django)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'conf.wsgi.application'


# Database Configuration (Configurée sans stockage /data externe)
# Note : Sur Render, sans disque persistant, les données seront réinitialisées à chaque redémarrage.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Kinshasa'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ==============================================================================
# CONFIGURATION DE SÉCURITÉ ET DE PRODUCTION AVANCÉE (PROD)
# ==============================================================================
if not DEBUG:
    # 1. Optimisation WhiteNoise et correction des fichiers manquants (.map)
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    # Indique à WhiteNoise de ne pas planter si un fichier source (.map) est introuvable
    WHITENOISE_MANIFEST_STRICT = False

    # 2. Sécurisation des cookies (Empêche l'interception et le vol de session)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'

    # 3. Redirection HTTPS et En-têtes de sécurité
    # Render gère le SSL/HTTPS de son côté (Reverse Proxy), on indique à Django de lui faire confiance
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    
    # En-têtes HTTP de protection du navigateur
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # HSTS (Strict-Transport-Security) : Force le navigateur à n'utiliser que le HTTPS
    SECURE_HSTS_SECONDS = 2592000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # 4. Protection contre le Clickjacking
    X_FRAME_OPTIONS = 'DENY'