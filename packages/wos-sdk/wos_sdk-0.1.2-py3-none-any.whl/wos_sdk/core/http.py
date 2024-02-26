import os
from typing import Any, Tuple
import requests
from ..type import WOSAPIResult, WOSPublishMessage

wos_endpoint = os.getenv("WOS_ENDPOINT", "localhost:15117")


def set_wos_endpoint(ep):
    global wos_endpoint
    wos_endpoint = ep


def get_wos_endpoint():
    global wos_endpoint
    return wos_endpoint


def get_http_url(path: str) -> str:
    return "http://" + get_wos_endpoint() + path


def wos_env():
    """
    Get wos environment data

    Example return:
    {
      "buildVersion": "0.0.0",
      "identifier": "DEBUG_IDENTIFIER",
      "debug": true,
      "isDocker": false,
      "isWindows": false,
      "isAndroid": false,
      "hostname": "home100-server",
      "homeDir": "/path/to/workspace",
      "rootDir": "/path/to/wos",
      "port": "15117",
      "fps": 60,
      "Interval": 16000000,
      "gui": true,
      "cpuModel": "Intel(R) Core(TM) i7-8700K CPU @ 3.70GHz",
      "gpuModel": "GP104 [GeForce GTX 1070] ",
      "memory": "15.54 GB",
      "docker": "Engine: 24.0.5 API:1.43",
      "model": ""
    }
    """

    response = requests.get(get_http_url("/api/env"))
    return response.json()


def wos_publish(resource: str, topic: str, data: Any) -> Tuple[bool, Any]:
    response = requests.post(
        get_http_url("/api/service/publish"),
        json=WOSPublishMessage(resource, topic, data).to_json(),
    )
    return response.status_code == 200, response.json()


def wos_request(resource: str, action: str, arguments: Any) -> Tuple[Any, str | None]:
    """
    Make a wos api request using http transport

    Parameters:
      - resource: The resource name
      - action: The action name
      - arguments: The request arguments

    Note: will block until request done

    """

    response = requests.post(
        get_http_url("/api/service/request/") + resource,
        json={"action": action, "arguments": arguments},
    )
    result = WOSAPIResult.from_json(response.json())

    return result.result, result.error
