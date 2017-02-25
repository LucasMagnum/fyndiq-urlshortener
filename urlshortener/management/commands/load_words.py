import os
import re

from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from ...models import Word


class Command(BaseCommand):
    help = 'Load words from file and save in database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            action='store_true',
            dest='wordlist',
            default=os.path.join(os.path.dirname(__file__), 'words.txt'),
            help='Path to word list',
        )

    def handle(self, *args, **options):
        filename = options['wordlist']

        self.stdout.write('Processing file %s' % options['wordlist'])

        cleaned_words = set()

        with open(filename) as opened_file:
            for line in opened_file.readlines():
                cleaned_word = self.clean_word(line.strip())

                if not cleaned_word:
                    continue

                cleaned_words.add(cleaned_word)

        try:
            with transaction.atomic():
                Word.objects.all().delete()
                self.stdout.write('Cleaned words table.')

                Word.objects.bulk_create(
                    Word(word=cleaned_word) for cleaned_word in cleaned_words
                )
                self.stdout.write('Inserted %s words in database' % Word.objects.count())

        except IntegrityError:
            self.stdout.write("Rollback was made.")
            self.stdout.write("The words wasn't loaded, check this file and try again.")

    def clean_word(self, word):
        return re.sub('[^\w]+', '', word)
