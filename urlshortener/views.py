from django import forms
from django.shortcuts import render, redirect

from . import shortener
from .exceptions import ShortenedURLNotFound


class ShortenerForm(forms.Form):
    url = forms.URLField(required=True)


def shortener_view(request, template_name='urlshortener/shortener.html'):
    form = ShortenerForm(request.POST or None)

    context = {
        'form': form
    }

    if form.is_valid():
        original_url = form.cleaned_data['url']
        shortened_url = shortener.generate_short_url(original_url)

        context.update({
            'shortened_url': shortened_url,
            'original_url': original_url
        })

    return render(request, template_name, context)


def redirect_view(request, shortened_url):
    try:
        redirect_url = shortener.get_original_url(shortened_url)
    except ShortenedURLNotFound:
        redirect_url = '/'

    return redirect(redirect_url)
