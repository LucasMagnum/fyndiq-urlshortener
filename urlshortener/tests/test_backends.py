import pytest

from ..backends.words import Shortener
from ..models import ShortenedURL, Word


@pytest.mark.django_db
def test_short_url_with_first_available_word_found():
    """When has available word should use it."""
    Word.objects.create(word='lawsuit', used=False)

    shortener = Shortener()
    short_url = shortener.generate_short_url('http://lawsuit.se/')

    assert short_url == 'lawsuit'


@pytest.mark.django_db
def test_get_orinal_url_with_valid_url():
    """Should return a original url for a valid url."""
    Word.objects.create(word='lawsuit', used=False)
    assert Word.objects.filter(used=True).count() == 0

    original_url = 'http://lawsuit.se/'

    shortener = Shortener()
    short_url = shortener.generate_short_url(original_url)

    assert Word.objects.filter(used=True).count() == 1

    assert shortener.get_original_url(short_url) == original_url


def test_extract_from_url():
    url = 'http://techcrunch.com/2012/12/28/pinterest-lawsuit/'

    shortener = Shortener()
    words = shortener.extract_words_from_url(url)

    expected_words = [
        'com', 'http', 'lawsuit', 'pinterest', 'techcrunch'
    ]

    assert sorted(words) == expected_words


@pytest.mark.django_db
def test_get_available_words_with_avaiable_word():
    """When has one word in database and it's not used, should return it."""
    Word.objects.create(word='lawsuit', used=False)

    words = ['lawsuit', 'http', 'pinterest']

    shortener = Shortener()
    available_words = shortener.get_available_words(words)

    assert list(available_words) == ['lawsuit']


@pytest.mark.django_db
def test_get_available_words_when_none_words_in_list():
    """If none of the words in the wordlist is a part of the URL, return the first."""
    Word.objects.create(word='lawsuit', used=True)
    Word.objects.create(word='other-word', used=False)

    words = ['lawsuit', 'http', 'pinterest']

    shortener = Shortener()
    available_words = shortener.get_available_words(words)

    assert list(available_words) == ['other-word']


@pytest.mark.django_db
def test_get_available_words_when_all_words_are_used():
    """When all words are used, should release one and use it again."""
    Word.objects.create(word='lawsuit', used=True)
    ShortenedURL.objects.create(shortened_url='lawsuit', original_url='test')
    ShortenedURL.objects.create(shortened_url='lawsuit2', original_url='test2')

    words = ['lawsuit', 'http', 'pinterest']

    assert ShortenedURL.objects.count() == 2

    shortener = Shortener()
    available_words = shortener.get_available_words(words)

    assert ShortenedURL.objects.count() == 1
    assert Word.objects.get(word='lawsuit').used is False
    assert list(available_words) == ['lawsuit']
