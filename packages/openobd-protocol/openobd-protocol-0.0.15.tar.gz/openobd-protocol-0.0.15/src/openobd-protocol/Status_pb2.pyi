from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNDEFINED: _ClassVar[StatusCode]
    AVAILABLE: _ClassVar[StatusCode]
    ACTIVE: _ClassVar[StatusCode]
    INTERRUPTED: _ClassVar[StatusCode]
    FINISHED: _ClassVar[StatusCode]
    FAILURE: _ClassVar[StatusCode]
UNDEFINED: StatusCode
AVAILABLE: StatusCode
ACTIVE: StatusCode
INTERRUPTED: StatusCode
FINISHED: StatusCode
FAILURE: StatusCode

class Status(_message.Message):
    __slots__ = ("success", "status_code", "status_description")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_CODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_code: StatusCode
    status_description: str
    def __init__(self, success: bool = ..., status_code: _Optional[_Union[StatusCode, str]] = ..., status_description: _Optional[str] = ...) -> None: ...
