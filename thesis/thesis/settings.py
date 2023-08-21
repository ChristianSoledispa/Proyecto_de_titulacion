
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-sy8vvn#o1h)84^lpnj!ctf0(g1$*btvherg@(1i#1+r061q#74"

DEBUG = True

ALLOWED_HOSTS = []

# CORS_ORIGIN_ALLOW_ALL = True
# for REACT
CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:9000",
]

CORS_ALLOWED_CREDENTIALS=True

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    # 'django.contrib.sites',
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "authentications",
    # "accounts",
    # "todo_api",
    # "user_api",
]

EXTERNAL_APPS = [
    # "tailwind",
    # 'theme',
    'django_browser_reload',
    "rest_framework",
    "rest_framework.authtoken",
    'drf_spectacular',
    # django allauth
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS 

# SITE_ID = 1
# LOGIN_REDIRECT_URL = "/scrapping"

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         # For each OAuth based provider, either add a ``SocialApp``
#         # (``socialaccount`` app) containing the required client
#         # credentials, or list them here:
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

# BASE_DIR = Path(__file__).resolve().parent

# TAILWINDCSS_CLI_FILE = BASE_DIR / 'tailwindcss-linux-x64'
# TAILWINDCSS_CONFIG_FILE = BASE_DIR / 'tailwind.config.js'

# For file mode
# TAILWINDCSS_OUTPUT_FILE = 'style.css'


# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#             #https://www.django-rest-framework.org/api-guide/settings/#default_authentication_classes
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
    
# }

REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Scrapping API',
    'DESCRIPTION': 'Based to locate websites and getting relevant authors in social medias (Dev: Christian Soledispa)',
    'VERSION': '1.5.1',
    'SERVE_INCLUDE_SCHEMA': False,
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
"django_browser_reload.middleware.BrowserReloadMiddleware",

]

LOGIN_URL = 'login/'
LOGOUT_URL = 'logout/'
ROOT_URLCONF = "thesis.urls"
TEMPLATES_DIR = os.path.join(BASE_DIR, 'authentications','templates')
# print("BASE_DIR",BASE_DIR / "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend',
# ]

WSGI_APPLICATION = "thesis.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': '1christthesis',
            'ENFORCE_SCHEMA': False,
            'CLIENT': {
                'host': 'mongodb+srv://heroe:heroe@cluster0.wkxtx.mongodb.net/1christthesis?retryWrites=true&w=majority'
            }  
        }
}

# AUTH_USER_MODEL = 'user_api.AppUser'



# MONGO_JWT CONFIG
# Minimal settings (all mandatory)
MANGO_JWT_SETTINGS = {
    "db_host": 'cluster0.wkxtx.mongodb.net', # Use srv host if connecting with MongoDB Atlas Cluster
    # "db_port": "some_db_port", # Don't include this field if connecting with MongoDB Atlas Cluster
    "db_name": "1christthesis",
    "db_user": "heroe",
    "db_pass": "heroe"
}






# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# TAILWIND_APP_NAME = 'theme'
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

# NPM_BIN_PATH = "/home/zukyo/.nvm/versions/node/v20.4.0/bin/npm"