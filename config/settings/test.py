from .base import *  # noqa


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'test.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = []
