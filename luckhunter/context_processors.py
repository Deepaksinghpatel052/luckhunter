import os

from django.templatetags.static import static


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
