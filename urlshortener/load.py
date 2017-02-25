import logging

from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


logger = logging.getLogger(__name__)


def load_shortener_from_backend():
    from .configs import get_configs

    urlshortener_configs = get_configs()

    logger.debug('urlshortener configs: {}.'.format(urlshortener_configs))

    try:
        backend = import_string(urlshortener_configs['backend'])
    except ImportError:
        raise ImproperlyConfigured(
            "You should set a valid backend for urlshortener"
        )

    shortener_class = getattr(backend, 'Shortener', None)
    assert shortener_class, "You backend must implement a Shortener class"

    return shortener_class()
