from typing import Any, Callable
from .type import (
    WOSServiceInfo,
)


class WOSServiceHandler:
    def handle_request(self, action: str, arguments: Any) -> tuple[Any, str | None]:
        return None, None

    def handle_action(
        self, action: str, arguments: Any, fb: Callable[[float, str], None]
    ) -> tuple[Any, str | None]:
        return None, None

    def handle_cancel(self, action: str, arguments: Any):
        pass

    def service_info(self) -> WOSServiceInfo:
        return WOSServiceInfo([], [], [])

    def resource_name(self) -> str:
        return ""
