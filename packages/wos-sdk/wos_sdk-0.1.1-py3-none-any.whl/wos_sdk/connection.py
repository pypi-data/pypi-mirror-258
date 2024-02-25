from .client import WOSClient
from .transport import WSTransport
from .http import wos_endpoint


def CreateWSClient(endpoint: str = wos_endpoint) -> WOSClient:
    wsEndpoint = "ws://" + endpoint + "/api/ws"
    transport = WSTransport(wsEndpoint)
    return WOSClient(transport)
