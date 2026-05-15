import logging
import sys

import requests

logging.basicConfig(stream=sys.stdout)

logger = logging.getLogger(__name__)


def is_valid_url(url):
    """
    Checks if the given URL is valid and reachable.
    Returns:
        (True, None) if valid.
        (False, "Error message") if invalid.
    """
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            return True, None
        return False, "Invalid URL"
    except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
        return False, "Unable to connect"
    except requests.exceptions.Timeout:
        return False, "Connection timed out"
    except requests.exceptions.MissingSchema:
        return False, "Invalid URL format"
