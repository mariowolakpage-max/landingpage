import os
from pathlib import Path
from dotenv import load_dotenv

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === Env ===
# Carrega .env na raiz do projeto (pensado para dev/local)
load_dotenv(BASE_DIR / ".env")

# === Segurança & Debug ===
# NUNCA deixe DEBUG=True em produção
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Secret Key obrigatória (defina no Render)
SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-dev-key-change-me")

# Hosts permitidos
# No Render, use algo como: .onrender.com,localhost,127.0.0.1
ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS",
    ".onrender.com,localhost,127.0.0.1"
).split(",") if h.strip()]

# CSRF Trusted (Django exige esquema)
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://*.onrender.com"
).split(",") if o.strip()]

# === Apps ===
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Seu app
    "core",

    # Opcional: helpers de template para Bootstrap 5 (se estiver usando)
    # "django_bootstrap5",
    # Opcional: compressor (se quiser minificar CSS/JS)
    # "django_compressor",
]

# === Middleware ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise: sirva estáticos direto do app em produção
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# === URLs/WSGI ===
ROOT_URLCONF = "setup.urls"
WSGI_APPLICATION = "setup.wsgi.application"

# === Templates ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # /templates na raiz do projeto
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# === Banco de Dados ===
# Fallback: SQLite. Se DATABASE_URL existir, usa ela (Postgres no Render).
# Requer dj-database-url no requirements.txt
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    from dj_database_url import config as dj_database_url_config
    DATABASES["default"] = dj_database_url_config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DEBUG  # em prod, força SSL no DB
    )

# === Password validators ===
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

<<<<<<< HEAD

# --- CONFIGURAÇÃO DE E-MAIL COM SENDGRID ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'

# Pega as credenciais do SendGrid do .env usando os.getenv()
EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

=======
# === I18N / Timezone ===
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
>>>>>>> fd91b9f747a36440807c2d20af3f46aa92636eea
USE_I18N = True
USE_TZ = True  # mantém o banco em UTC (recomendado)

# === Static files (obrigatório para collectstatic) ===
# Em produção, o Django coletará tudo em STATIC_ROOT
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Se você possui arquivos locais em /static (CSS/JS/Imagens do projeto)
STATICFILES_DIRS = []
_static_dir = BASE_DIR / "static"
if _static_dir.exists():
    STATICFILES_DIRS.append(_static_dir)

# Django 4.2+ recomenda STORAGES ao invés de STATICFILES_STORAGE
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# === (Opcional) django-compressor – se habilitar no INSTALLED_APPS ===
# COMPRESS_ENABLED = not DEBUG
# COMPRESS_URL = STATIC_URL
# COMPRESS_ROOT = STATIC_ROOT

# === Arquivos de mídia (se precisar) ===
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# === Segurança extra quando DEBUG=False ===
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True  # redireciona http->https no Render
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Ajuste conforme necessidade do seu caso
    # SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7  # 1 semana
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

# === Log básico (útil em produção) ===
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}

# === Primary key default ===
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
