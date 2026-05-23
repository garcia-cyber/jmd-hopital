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

# ... (Garde ton bloc TEMPLATES inchangé) ...

WSGI_APPLICATION = 'conf.wsgi.application'


# Database Configuration (Configurée sans stockage /data externe)
# Note : Sur Render, sans disque persistant, les données seront réinitialisées à chaque redémarrage.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ... (Garde ton bloc AUTH_PASSWORD_VALIDATORS inchangé) ...


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
# CONFIGURATION DE SÉCURITÉ AVANCÉE (PROD)
# ==============================================================================
if not DEBUG:
    # 1. Optimisation WhiteNoise pour la prod
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

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

    # 4. Protection contre le Clickjacking (Déjà renforcé par le middleware)
    X_FRAME_OPTIONS = 'DENY'