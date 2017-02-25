from .. import configs


def test_default_backend_is_words():
    """By default our backend is words."""
    assert configs.default_backend == "urlshortener.backends.words"


def test_default_configs_use_default_backend():
    """Default configs should use default backend."""
    assert configs.default_configs['backend'] == configs.default_backend


def test_app_returns_from_settings_when_it_is_defined(settings):
    """Should return from settings when it's defined."""
    test_backend = 'test.backend.test'
    settings.URLSHORTENER_CONFIGS = {'backend': test_backend}

    assert configs.get_configs()['backend'] == test_backend


def test_app_returns_default_config_when_isnt_set_in_settings(settings):
    """When settings doesn't define a URLSHORTENER_CONFIGS should return default."""
    assert getattr(settings, 'URLSHORTENER_CONFIGS', None) is None
    assert configs.get_configs() == configs.default_configs
