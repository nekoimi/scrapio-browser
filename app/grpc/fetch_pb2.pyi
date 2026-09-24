from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FetchRequest(_message.Message):
    __slots__ = ("url", "timeout")
    URL_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    url: str
    timeout: int
    def __init__(self, url: _Optional[str] = ..., timeout: _Optional[int] = ...) -> None: ...

class FetchResponse(_message.Message):
    __slots__ = ("success", "html", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    HTML_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: bool
    html: str
    error: str
    def __init__(self, success: _Optional[bool] = ..., html: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class BrowserAction(_message.Message):
    __slots__ = ("type", "selector", "value", "script", "timeout_ms")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SELECTOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    type: str
    selector: str
    value: str
    script: str
    timeout_ms: int
    def __init__(self, type: _Optional[str] = ..., selector: _Optional[str] = ..., value: _Optional[str] = ..., script: _Optional[str] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class BrowserJobRequest(_message.Message):
    __slots__ = ("protocol_version", "request_id", "url", "profile", "recipe", "timeout_ms", "actions", "outputs", "headers", "close_page")
    class HeadersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    RECIPE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    CLOSE_PAGE_FIELD_NUMBER: _ClassVar[int]
    protocol_version: str
    request_id: str
    url: str
    profile: str
    recipe: str
    timeout_ms: int
    actions: _containers.RepeatedCompositeFieldContainer[BrowserAction]
    outputs: _containers.RepeatedScalarFieldContainer[str]
    headers: _containers.ScalarMap[str, str]
    close_page: bool
    def __init__(self, protocol_version: _Optional[str] = ..., request_id: _Optional[str] = ..., url: _Optional[str] = ..., profile: _Optional[str] = ..., recipe: _Optional[str] = ..., timeout_ms: _Optional[int] = ..., actions: _Optional[_Iterable[_Union[BrowserAction, _Mapping]]] = ..., outputs: _Optional[_Iterable[str]] = ..., headers: _Optional[_Mapping[str, str]] = ..., close_page: _Optional[bool] = ...) -> None: ...

class BrowserCookie(_message.Message):
    __slots__ = ("name", "value", "domain", "path")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    domain: str
    path: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ..., domain: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class BrowserJobResponse(_message.Message):
    __slots__ = ("success", "protocol_version", "request_id", "error_code", "error", "html", "text", "json", "screenshot", "cookies", "duration_ms")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    HTML_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    JSON_FIELD_NUMBER: _ClassVar[int]
    SCREENSHOT_FIELD_NUMBER: _ClassVar[int]
    COOKIES_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    protocol_version: str
    request_id: str
    error_code: str
    error: str
    html: str
    text: str
    json: str
    screenshot: bytes
    cookies: _containers.RepeatedCompositeFieldContainer[BrowserCookie]
    duration_ms: int
    def __init__(self, success: _Optional[bool] = ..., protocol_version: _Optional[str] = ..., request_id: _Optional[str] = ..., error_code: _Optional[str] = ..., error: _Optional[str] = ..., html: _Optional[str] = ..., text: _Optional[str] = ..., json: _Optional[str] = ..., screenshot: _Optional[bytes] = ..., cookies: _Optional[_Iterable[_Union[BrowserCookie, _Mapping]]] = ..., duration_ms: _Optional[int] = ...) -> None: ...

class BrowserHealthRequest(_message.Message):
    __slots__ = ("protocol_version", "request_id")
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    protocol_version: str
    request_id: str
    def __init__(self, protocol_version: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...

class BrowserHealthResponse(_message.Message):
    __slots__ = ("ready", "protocol_version", "request_id", "message")
    READY_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_VERSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ready: bool
    protocol_version: str
    request_id: str
    message: str
    def __init__(self, ready: _Optional[bool] = ..., protocol_version: _Optional[str] = ..., request_id: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
