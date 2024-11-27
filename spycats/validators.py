import logging
from typing import Callable

import requests.exceptions

from spycats.utils import get_breeds_from_api

logger = logging.getLogger()
def validate_breed_name(name: str, error_to_raise: Callable) -> bool:
    try:
        breeds = get_breeds_from_api()
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot fetch breed data from external API: {e}")

    breed_names = {breed["name"] for breed in breeds}

    if not name.lower() in breed_names:
        raise error_to_raise(
            f"Breed {name} probably does not exist"
        )
