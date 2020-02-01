"""
Django settings for seismic_site project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import dj_database_url
from configurations import Configuration, values

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Base(Configuration):
    DEBUG = False

    SECRET_KEY = values.Value()

    ALLOWED_HOSTS = []

    INSTALLED_APPS = [
        # django apps
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # third-party apps
        "rest_framework",
        "ckeditor",
        # project apps
        "buildings",
        "pages",
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
    ]

    ROOT_URLCONF = "seismic_site.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
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

    WSGI_APPLICATION = "seismic_site.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    DATABASES = {"default": dj_database_url.config(conn_max_age=600)}

    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = values.Value(default="en-us")
    TIME_ZONE = "UTC"
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/

    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "./public/static")
    # STATICFILES_DIRS = (
    #     os.path.join(BASE_DIR, 'static'),
    # )
    STATICFILES_STORAGE = (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "./public/media")

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
        ]
    }


class Dev(Base):
    DEBUG = True
    SECRET_KEY = "secret"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


class Test(Base):
    DEBUG = True
    SECRET_KEY = "secret"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'testdbfile.sqlite3',
        }
    }


class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS = values.ListValue(default=[".code4.ro"])
