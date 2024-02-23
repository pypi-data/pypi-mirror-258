import logging
from typing import Dict, Any

from posthog import Posthog

from codeflash.api.cfapi import get_user_id
from codeflash.version import __version__, __version_tuple__

_posthog = Posthog(
    project_api_key="phc_aUO790jHd7z1SXwsYCz8dRApxueplZlZWeDSpKc5hol", host="https://us.posthog.com"
)


def ph(event: str, properties: Dict[str, Any] = None) -> None:
    """
    Log an event to PostHog.
    :param event: The name of the event.
    :param properties: A dictionary of properties to attach to the event.
    """

    if properties is None:
        properties = {}

    properties["cli_version"] = __version__
    properties["cli_version_tuple"] = __version_tuple__

    user_id = get_user_id()

    if user_id:
        _posthog.capture(
            distinct_id=user_id,
            event=event,
            properties=properties,
        )
    else:
        logging.debug("Failed to log event to PostHog: User ID could not be retrieved.")
