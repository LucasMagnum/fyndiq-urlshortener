from django.conf import settings

default_backend = 'urlshortener.backends.words'
default_configs = {
    'backend': default_backend,
}


def get_configs():
    """Return configs from settings or use default."""

    configs = getattr(settings, 'URLSHORTENER_CONFIGS', default_configs)
    assert 'backend' in configs, "Invalid configuration for urlshortener"

    return configs
