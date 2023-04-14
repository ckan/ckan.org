"""
Django settings for ckanorg project.
Generated by 'django-admin startproject' using Django 3.1.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'streams',
    'menus',
    'contact',
    'managers',
    'ckan_pages',
    'blog',
    'events',
    'dashboard',
    'faq',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.settings',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'wagtailcache',
    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.sites',

    'wagtailmetadata',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    'captcha',
    'wagtailcaptcha',
    'wagtailcodeblock',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/admin/'

ACCOUNT_FORMS = {
    'signup': 'home.forms.CkanorgSignupForm',
}

MIDDLEWARE = [
    'wagtailcache.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'wagtailcache.cache.FetchFromCacheMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
        'KEY_PREFIX': 'wagtailcache',
        'TIMEOUT': 3600, # one hour (in seconds)
    }
}

X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'ckanorg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'ckanorg.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Wagtail settings

WAGTAIL_SITE_NAME = "ckanorg"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'https://ckan.org'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.eu-central-1.amazonaws.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'AKIAUWX42BAVQ3UFZFUU'
DEFAULT_FROM_EMAIL = 'noreply@ckan.org'

ACCOUNT_ADAPTER = 'ckan_pages.adapter.NoNewUsersAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_BLACKLIST = ['admin',]

DEBUG = False

GITHUB_CACHE_DIR = '{}/cache'.format(BASE_DIR)

ALLOWED_HOSTS = ['*']

WAGTAIL_APPEND_SLASH = False

with open(BASE_DIR + '/../config/secret.txt') as f:
    data = f.read().strip().split(',')
    SECRET_KEY = data[0]
    EMAIL_HOST_PASSWORD = data[1]
    DB_HOST = data[2]
    DB_PASS = data[3]
    RECAPTCHA_PUBLIC_KEY = data[4]
    RECAPTCHA_PRIVATE_KEY = data[5]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ckanorg',
        'USER': 'ckanorg',
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'PORT': 5432,
    }
}

# Wagtailcode block settings
WAGTAIL_CODE_BLOCK_THEME = 'coy'
WAGTAIL_CODE_BLOCK_LINE_NUMBERS = True
WAGTAIL_CODE_BLOCK_LANGUAGES = (
    ('bash', 'Bash/Shell'),
    ('css', 'CSS'),
    ('diff', 'diff'),
    ('html', 'HTML'),
    ('javascript', 'Javascript'),
    ('json', 'JSON'),
    ('python', 'Python'),
    ('scss', 'SCSS'),
    ('yaml', 'YAML'),
)