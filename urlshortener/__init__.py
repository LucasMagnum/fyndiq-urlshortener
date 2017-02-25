from django.utils.functional import SimpleLazyObject

from .load import load_shortener_from_backend


__all__ = ['shortener']


shortener = SimpleLazyObject(load_shortener_from_backend)
