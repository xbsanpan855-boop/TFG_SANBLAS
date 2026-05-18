"""
Django settings for sanblas project.
"""

from pathlib import Path
import os

# 1. RUTAS BÁSICAS
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. SEGURIDAD (En desarrollo)
SECRET_KEY = 'django-insecure-nfcg!%l%8%0ig)g@!j73k%r2akgy51n)=9!=q0_dzd!qr#e)0f'
DEBUG = False
ALLOWED_HOSTS = ['.render.com', 'localhost', '127.0.0.1']

# 3. APLICACIONES
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app', # Tu aplicación de San Blas
]

# 4. MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sanblas.urls'

# 5. PLANTILLAS (TEMPLATES)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Al ser APP_DIRS: True, busca dentro de app/templates/
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

WSGI_APPLICATION = 'sanblas.wsgi.application'

# 6. BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 8. IDIOMA Y HORA (Configurado para España)
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# 9. ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
STATIC_URL = 'static/'

# IMPORTANTE: Cambiamos el nombre de STATIC_ROOT para que no choque con tu carpeta 'static'
# Esto solo se usará cuando lances la web a internet (collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Esto le dice a Django que busque en carpetas static adicionales si las hubiera
STATICFILES_DIRS = []

# 10. ARCHIVOS MULTIMEDIA (Fotos de productos)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 11. MODELO DE USUARIO PERSONALIZADO
AUTH_USER_MODEL = 'app.Usuario'

# 12. REDIRECCIONES DE LOGIN
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'  