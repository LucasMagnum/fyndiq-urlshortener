from unittest import mock

import pytest

from django.core.exceptions import ImproperlyConfigured

from ..load import load_shortener_from_backend


class Shortener(object):
    """Fake shortener for thest."""
    name = "fake-shortener"


@mock.patch('urlshortener.configs.get_configs')
def test_raise_error_when_backend_path_is_invalid(get_configs_mock):
    get_configs_mock.return_value = {
        'backend': 'some-invalid.backend'
    }

    with pytest.raises(ImproperlyConfigured):
        load_shortener_from_backend()


@mock.patch('urlshortener.configs.get_configs')
def test_raise_error_when_backend_doesnt_has_shortener_class(get_configs_mock):
    get_configs_mock.return_value = {
        'backend': 'urlshortener.configs'
    }

    with pytest.raises(AssertionError):
        load_shortener_from_backend()


@mock.patch('urlshortener.configs.get_configs')
def test_return_shortener_class_from_backend(get_configs_mock):
    get_configs_mock.return_value = {
        'backend': 'urlshortener.tests.test_load'
    }

    shortener = load_shortener_from_backend()

    assert shortener.name == "fake-shortener"
