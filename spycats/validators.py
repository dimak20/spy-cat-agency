import logging
from typing import Callable

import requests.exceptions

from spycats.utils import get_breeds_from_api

logger = logging.getLogger()
def validate_breed_name(name: str, error_to_raise: Callable) -> None | Exception:
    """Validate if the breed name exists in the external API data."""
    try:
        breeds = get_breeds_from_api()
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot fetch breed data from external API: {e}")

    breed_names = {breed["name"].lower() for breed in breeds}

    if not name.lower() in breed_names:
        raise error_to_raise(
            f"Breed {name} probably does not exist"
        )

    return None
