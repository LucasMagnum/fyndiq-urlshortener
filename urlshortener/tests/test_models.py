import pytest

from django.db import IntegrityError

from ..models import Word, ShortenedURL


@pytest.mark.django_db
def test_create_word_model():
    word = Word.objects.create(word="test")
    assert word.word == "test"


@pytest.mark.django_db
def test_word_should_be_unique():
    with pytest.raises(IntegrityError):
        Word.objects.create(word="test")
        Word.objects.create(word="test")


@pytest.mark.django_db
def test_create_shortened_url():
    shortned = ShortenedURL.objects.create(
        shortened_url="test",
        original_url="url"
    )

    assert shortned.shortened_url == "test"
    assert shortned.original_url == "url"


@pytest.mark.django_db
def test_create_shortened_url_shortned_is_unique():
    with pytest.raises(IntegrityError):
        ShortenedURL.objects.create(shortened_url="test", original_url="url")
        ShortenedURL.objects.create(shortened_url="test", original_url="url")
