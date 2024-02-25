import threading
from typing import Any, Callable, Tuple
from uuid import uuid4
from .type import (
    WOSAPIFeedback,
    WOSAPIMessage,
    WOSAPIRequest,
    WOSAPIResult,
    WOSPublishMessage,
)
from .logger import logger
from .constant import Op
from .transport import WOSTransport
from .service import WOSServiceHandler


class WOSRegisterServiceRequest:
    def __init__(self, id: str) -> None:
        self.id = id
        self.success = False
        self.err = None
        self.event = threading.Event()

    def wait(self):
        self.event.wait()

    def on_result(self, success: bool, err: str | None):
        self.success = success
        self.err = err
        self.event.set()


class WOSRequestHandler:

    def __init__(self) -> None:
        self.completed = threading.Event()
        self.result = None
        self.err = None

    def on_result(self, result: Any, err: str):
        self.result = result
        self.err = err
        self.completed.set()

    def on_feedback(self, progress: float, status: str):
        pass

    def wait(self):
        self.completed.wait()


class WOSClient:

    def __init__(self, transport: WOSTransport) -> None:
        self.transport = transport
        self.t = None
        self.transport.bind(self._receive_message)
        self.requestHandler: dict[str, WOSRequestHandler] = {}
        self.serviceHandle: WOSServiceHandler | None = None

        self.register_service_request = None
        self.subscriptions = {}

    def run(self):
        """run transport connection, will block code execution forever"""
        self.transport.run()

    def connect(self):
        """connect to wos, will block until connection either success or failed

        @return bool: connection success or failed

        """
        self.t = threading.Thread(target=self.run)
        self.t.start()
        return self.transport.wait_connected()

    def disconnect(self):
        """disconnect from wos, will block until connection disconnected"""
        self.transport.stop()
        if self.t != None:
            self.t.join()
            logger.debug("websocket thread complete")

    def subscribe(self, resource: str, cb: Callable[[WOSPublishMessage], None]):
        if not resource in self.subscriptions:
            self.subscriptions[resource] = {}
            self.transport.send(
                WOSAPIMessage(str(uuid4()), Op.OpSubscribe, resource, {})
            )
        self.subscriptions[resource][cb.__hash__()] = cb

    def unsubscribe(self, resource: str, cb: Callable[[WOSPublishMessage], None]):
        if resource in self.subscriptions:
            if cb.__hash__ in self.subscriptions[resource]:
                self.subscriptions.pop(cb.__hash__())
            if len(self.subscriptions[resource]) == 0:
                self.transport.send(
                    WOSAPIMessage(str(uuid4()), Op.OpUnsubscribe, resource, {})
                )
                self.subscriptions.pop(resource)

    def run_request(
        self, resource: str, action: str, args: Any
    ) -> Tuple[Any | None, str | None]:
        id = str(uuid4())
        handler = WOSRequestHandler()
        self.requestHandler[id] = handler
        self.transport.send(
            WOSAPIMessage(id, Op.OpRequest, resource, WOSAPIRequest(action, args))
        )
        handler.wait()
        return handler.result, handler.err

    def run_action(
        self, resource: str, action: str, args: Any, fb: Callable[[float, str], None]
    ) -> Tuple[Any | None, str | None]:
        id = str(uuid4())
        handler = WOSRequestHandler()
        handler.on_feedback = lambda progress, status: fb(progress, status)
        self.requestHandler[id] = handler
        self.transport.send(
            WOSAPIMessage(id, Op.OpAction, resource, WOSAPIRequest(action, args))
        )
        handler.wait()
        return handler.result, handler.err

    def register_service(self, handle: WOSServiceHandler) -> bool:
        if self.serviceHandle != None:
            return False
        id = str(uuid4())
        self.serviceHandle = handle
        self.register_service_request = WOSRegisterServiceRequest(id)
        info = handle.service_info()
        self.transport.send(
            WOSAPIMessage(id, Op.OpRegisterService, handle.resource_name(), info)
        )
        self.register_service_request.wait()
        return True

    def remove_service(self):
        if self.serviceHandle != None:
            self.transport.send(
                WOSAPIMessage(
                    "", Op.OpRemoveService, self.serviceHandle.resource_name()
                )
            )
            self.serviceHandle = None
            if (
                self.register_service_request != None
                and not self.register_service_request.event.is_set()
            ):
                self.register_service_request.on_result(False, "Removed service")
                self.register_service_request = None

    def _receive_message(self, msg: WOSAPIMessage):
        thread = threading.Thread(target=self._handle_message, args=(msg,))
        thread.start()

    def _handle_message(self, msg: WOSAPIMessage):
        if msg.op == Op.OpPublish:
            if msg.resource in self.subscriptions:
                for k in self.subscriptions[msg.resource]:
                    self.subscriptions[msg.resource][k](msg.get_publish_message())

        if msg.op == Op.OpRequest:
            if self.serviceHandle != None:
                req = msg.get_api_request()
                result, err = self.serviceHandle.handle_request(
                    req.action, req.arguments
                )
                if err == None:
                    self.transport.send(
                        WOSAPIMessage(
                            msg.id, Op.OpResult, msg.resource, WOSAPIResult("", result)
                        )
                    )
                else:
                    self.transport.send(
                        WOSAPIMessage(msg.id, Op.OpError, msg.resource, err)
                    )
        if msg.op == Op.OpAction:
            if self.serviceHandle != None:
                req = msg.get_api_request()
                result, err = self.serviceHandle.handle_action(
                    req.action,
                    req.arguments,
                    lambda p, s: self.transport.send(
                        WOSAPIMessage(
                            msg.id, Op.OpFeedback, msg.resource, WOSAPIFeedback(p, s)
                        )
                    ),
                )
                if err == None:
                    self.transport.send(
                        WOSAPIMessage(
                            msg.id, Op.OpResult, msg.resource, WOSAPIResult("", result)
                        )
                    )
                else:
                    self.transport.send(
                        WOSAPIMessage(msg.id, Op.OpError, msg.resource, err)
                    )
        if msg.op == Op.OpCancel:
            if self.serviceHandle != None:
                req = msg.get_api_request()
                self.serviceHandle.handle_cancel(req.action, req.arguments)

        if msg.op == Op.OpResult:
            if msg.id in self.requestHandler:
                handle = self.requestHandler[msg.id]
                req = msg.get_api_result()
                handle.on_result(req.result, req.error)
                self.requestHandler.pop(msg.id)

        if msg.op == Op.OpFeedback:
            if msg.id in self.requestHandler:
                handle = self.requestHandler[msg.id]
                req = msg.get_api_feedback()
                handle.on_feedback(req.progress, req.status)

        if msg.op == Op.OpError:
            logger.warn(
                "Receive Error (resource: %s): %s", msg.resource, msg.get_data_string()
            )
            if (
                self.register_service_request != None
                and msg.id == self.register_service_request.id
            ):
                self.register_service_request.on_result(False, msg.data)
                self.register_service_request = None

        if msg.op == Op.OpAck:
            if (
                self.register_service_request != None
                and msg.id == self.register_service_request.id
            ):
                self.register_service_request.on_result(True, None)
                self.register_service_request = None
