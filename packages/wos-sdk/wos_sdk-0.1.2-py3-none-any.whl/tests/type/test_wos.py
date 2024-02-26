from wos_sdk.type import (
    WOSAPIFeedback,
    WOSAPIResult,
    WOSAPIRequest,
    WOSPublishMessage,
    WOSServiceInfo,
    WOSAPIMessage,
)


def test_wos_api_feedback():
    obj = {"progress": 0.5, "status": "InProgress"}
    feedback = WOSAPIFeedback.from_json(obj)
    assert feedback.progress == 0.5
    assert feedback.status == "InProgress"
    assert feedback.to_json() == obj


def test_wos_api_result():
    result_obj = {"error": "", "result": "Success"}
    result = WOSAPIResult.from_json(result_obj)
    assert result.error == ""
    assert result.result == "Success"
    assert result.to_json() == result_obj


def test_wos_api_request():
    request_obj = {"action": "getData", "arguments": {"param1": "value1"}}
    request = WOSAPIRequest.from_json(request_obj)
    assert request.action == "getData"
    assert request.arguments == {"param1": "value1"}
    assert request.to_json() == request_obj


def test_wos_publish_message():
    message_obj = {"resource": "sensor", "topic": "temperature", "message": "23"}
    message = WOSPublishMessage.from_json(message_obj)
    assert message.resource == "sensor"
    assert message.topic == "temperature"
    assert message.message == "23"
    assert message.to_json() == message_obj


def test_wos_service_info():
    service_info_obj = {
        "topics": ["temperature", "humidity"],
        "requests": ["getData"],
        "actions": ["setData"],
    }
    service_info = WOSServiceInfo.from_json(service_info_obj)
    assert service_info.topics == ["temperature", "humidity"]
    assert service_info.requests == ["getData"]
    assert service_info.actions == ["setData"]
    assert service_info.to_json() == service_info_obj


def test_wos_api_message():
    api_message_obj = {
        "id": "1234",
        "op": "publish",
        "resource": "sensor",
        "data": {"resource": "sensor", "topic": "temperature", "message": "23"},
    }
    api_message = WOSAPIMessage.from_json(api_message_obj)
    assert api_message.id == "1234"
    assert api_message.op == "publish"
    assert api_message.resource == "sensor"
    assert isinstance(api_message.get_publish_message(), WOSPublishMessage)
    assert (
        api_message.to_json()
        == '{"id": "1234", "op": "publish", "resource": "sensor", "data": {"resource": "sensor", "topic": "temperature", "message": "23"}}'
    )
