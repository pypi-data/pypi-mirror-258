from .client import WOSClient
from ..transport import WSTransport
from .http import get_wos_endpoint


def CreateWSClient(endpoint: str = get_wos_endpoint()) -> WOSClient:
    """
    Factory function to create a wos client using websocket transports

    Parameters:
      - Endpoint: The endpoint to connect. default: WOS_ENDPOINT env variable or localhost:15117

    Return:
      - WOSClient object
    """
    wsEndpoint = "ws://" + endpoint + "/api/ws"
    transport = WSTransport(wsEndpoint)
    return WOSClient(transport)
