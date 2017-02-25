from django.db import models


class ShortenedURL(models.Model):
    """This models is used to persist shortned url in database."""
    shortened_url = models.CharField(max_length=80, db_index=True, unique=True)
    original_url = models.URLField(max_length=80)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return "<ShortenedURL from: {original} to: {short}".format(
            original=self.original_url, short=self.shortened_url
        )


class Word(models.Model):
    """This model is used by words backends to keep all words in database."""
    word = models.CharField(max_length=80, db_index=True, unique=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return "<Word: {word}>".format(word=self.word)
