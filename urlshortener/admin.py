from django.contrib import admin

from .models import ShortenedURL, Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ['word']
    search_fields = ['word']


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ['shortened_url', 'original_url']
    search_fields = ['shortened_url']
