import os
from typing import Any, Tuple
import requests

from .type import WOSAPIResult


wos_endpoint = os.getenv("WOS_ENDPOINT", "localhost:15117")


def set_wos_endpoint(ep):
    wos_endpoint = ep


def wos_request(resource: str, action: str, arguments: Any) -> Tuple[Any, str | None]:
    """
    Make a wos api request using http transport

    Parameters:
      - resource: The resource name
      - action: The action name
      - arguments: The request arguments

    Will block until
    """

    response = requests.post(
        "http://" + wos_endpoint + "/api/service/request/" + resource,
        json={"action": action, "arguments": arguments},
    )
    result = WOSAPIResult.from_json(response.json())

    return result.result, result.error
