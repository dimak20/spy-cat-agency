import requests
from django.conf import settings
from django.core.cache import cache

BREEDS_API = settings.BREED_NAMES_API


def get_breeds_from_api(
        cache_key: str | None = "static_key",
        cache_timeout: int | None = 600
) -> set:
    """Fetch all breeds from an external API"""
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    response = requests.get(BREEDS_API)
    response.raise_for_status()
    data = response.json()
    cache.set(cache_key, data, timeout=cache_timeout)

    return data
