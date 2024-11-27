import logging
from time import sleep

import requests
from django.conf import settings
from django.core.cache import cache

BREEDS_API = settings.BREED_NAMES_API

logger = logging.getLogger()


def get_breeds_from_api(
        cache_key: str | None = "static_key",
        cache_timeout: int | None = 600,
        max_retries: int | None = 5,
        delay: int | None = 2
) -> dict:
    """
    Fetch all breeds from an external API
    and set value to cache
    """
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(BREEDS_API)
            response.raise_for_status()
            data = response.json()

            cache.set(cache_key, data, timeout=cache_timeout)
            return data

        except requests.exceptions.RequestException as e:
            retries += 1
            logger.info(f"Attempt {retries} to fetch breed data failed: {e}")

            if retries == max_retries:
                logger.error("Max retries reached. Could not fetch breed data.")
                raise

            sleep(delay)
