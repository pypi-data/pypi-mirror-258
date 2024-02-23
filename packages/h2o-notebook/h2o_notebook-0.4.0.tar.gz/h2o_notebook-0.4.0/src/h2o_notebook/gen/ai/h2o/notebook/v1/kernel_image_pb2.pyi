from google.api import resource_pb2 as _resource_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KernelImage(_message.Message):
    __slots__ = ("name", "display_name", "type", "image", "disabled", "create_time", "update_time")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNSPECIFIED: _ClassVar[KernelImage.Type]
        TYPE_PYTHON: _ClassVar[KernelImage.Type]
        TYPE_R: _ClassVar[KernelImage.Type]
        TYPE_SPARK_PYTHON: _ClassVar[KernelImage.Type]
        TYPE_SPARK_R: _ClassVar[KernelImage.Type]
    TYPE_UNSPECIFIED: KernelImage.Type
    TYPE_PYTHON: KernelImage.Type
    TYPE_R: KernelImage.Type
    TYPE_SPARK_PYTHON: KernelImage.Type
    TYPE_SPARK_R: KernelImage.Type
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    type: KernelImage.Type
    image: str
    disabled: bool
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., type: _Optional[_Union[KernelImage.Type, str]] = ..., image: _Optional[str] = ..., disabled: bool = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
