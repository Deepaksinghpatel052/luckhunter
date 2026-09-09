import os

from django.conf import settings
from django.templatetags.static import static


def base_url(request):
    """Fallback BASE_URL for any view that forgets to pass it explicitly.
    An explicit 'BASE_URL' in a view's own context still takes precedence."""
    return {'BASE_URL': settings.BASE_URL}


def product_placeholder(request):
    """Expose the fallback image URL used when a product's stored Image
    file is missing on disk, so any template can reference it (e.g. in an
    <img onerror="..."> handler)."""
    value = os.environ.get(
        'PRODUCT_PLACEHOLDER_IMAGE_URL',
        'static/product_placeholder/placeholder.png',
    )
    if value.startswith(('http://', 'https://', '/')):
        url = value
    else:
        url = static(value.split('static/', 1)[-1])
    return {'PRODUCT_PLACEHOLDER_IMAGE_URL': url}
