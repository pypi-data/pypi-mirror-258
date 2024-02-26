import pytest
from unittest.mock import Mock, patch
from wos_sdk.core import WOSClient, WOSServiceHandler
from wos_sdk.type import WOSAPIMessage, WOSAPIRequest, WOSAPIResult, WOSPublishMessage
from wos_sdk.type.constant import Op
from wos_sdk.transport import WOSTransport


@pytest.fixture
def mock_transport():
    return Mock(spec=WOSTransport)


@pytest.fixture
def wos_client(mock_transport):
    return WOSClient(transport=mock_transport)


@pytest.fixture
def mock_service_handler():
    handler = Mock(spec=WOSServiceHandler)
    handler.resource_name.return_value = "test_resource"
    handler.service_info.return_value = {}
    return handler


def test_connect_disconnect(wos_client, mock_transport):
    mock_transport.wait_connected.return_value = True
    assert wos_client.connect() == True
    wos_client.disconnect()
    mock_transport.stop.assert_called_once()


def test_subscribe(wos_client, mock_transport):
    callback = Mock()
    resource = "test_resource"
    wos_client.subscribe(resource, callback)
    mock_transport.send.assert_called_once()
    assert resource in wos_client.subscriptions


def test_unsubscribe(wos_client, mock_transport):
    callback = Mock()
    resource = "test_resource"
    # Simulate subscription
    assert resource not in wos_client.subscriptions
    wos_client.subscribe(resource, callback)
    assert resource in wos_client.subscriptions
    print(wos_client.subscriptions)
    wos_client.unsubscribe(resource, callback)
    print(wos_client.subscriptions)
    assert resource not in wos_client.subscriptions
    assert mock_transport.send.call_count == 2  # Called during unsubscribe


def test_remove_service(wos_client, mock_transport, mock_service_handler):
    # Simulate service registration
    wos_client.serviceHandle = mock_service_handler
    wos_client.remove_service()
    mock_transport.send.assert_called_once()
    assert wos_client.serviceHandle is None
