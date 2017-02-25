import re

import nltk

from ..models import ShortenedURL, Word
from .base import ShortenerBase


class Shortener(ShortenerBase):
    """
    The shortened URLs will have the form

    http://myurlshortener.com/<word>/ where <word> is a word from the english language.

    Rules:

    * It should pick the first word in the wordlist that is a part of this URL.
    * If none of the words in the wordlist is a part of the URL, any word should be used
    * If all words that are part of the URL are already used, any word should be used
    * When all the words have been used, the oldest existing key/URL should be deleted
        and that key should be reused for new URL submissions.
    """
    def generate_short_url(self, url):
        words_url = self.extract_words_from_url(url)
        available_words = self.get_available_words(words_url)

        word = available_words[0]

        self.save_shortened_url(word, url)
        return word

    def extract_words_from_url(self, url):
        """Extract words from url, ignore only digits words."""
        words = nltk.tokenize.WordPunctTokenizer().tokenize(url)

        cleaned_words = set()

        for word in words:
            cleaned_word = re.sub('[^\w]+', '', word)

            if not cleaned_word or cleaned_word.isdigit():
                continue

            cleaned_words.add(cleaned_word)

        return cleaned_words

    def get_available_words(self, words):
        """Get words that wasn't used yet."""
        remaining_words = Word.objects.filter(used=False)

        if not remaining_words.exists():
            self.release_oldest_shortened_url()
            return self.get_available_words(words)

        available_words = Word.objects.filter(
            word__in=words, used=False
        ).values_list('word', flat=True)

        if not available_words.exists():
            return remaining_words.values_list('word')[0]

        return available_words

    def release_oldest_shortened_url(self):
        """Release the oldest shortened url."""
        shortened_url = ShortenedURL.objects.order_by(
            'created_at'
        ).first()

        if shortened_url:
            Word.objects.filter(
                word=shortened_url.shortened_url
            ).update(used=False)

            shortened_url.delete()

    def get_original_url(self, shortened_url):
        """Return original url for shortened_url."""
        try:
            shortened = ShortenedURL.objects.get(
                shortened_url=shortened_url,
            )
        except ShortenedURL.DoesNotExist:
            raise ValueError('ShortenedURL not found')

        return shortened.original_url

    def save_shortened_url(self, word, url):
        ShortenedURL.objects.create(
            shortened_url=word,
            original_url=url
        )
        Word.objects.filter(word=word).update(used=True)
