from google.api import resource_pb2 as _resource_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Kernel(_message.Message):
    __slots__ = ("name", "display_name", "image", "template", "notebook_kernel_spec", "environmental_variables", "creator", "creator_display_name", "state", "type", "current_task", "current_task_sequence_number", "task_queue_size", "last_activity_time", "create_time")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNSPECIFIED: _ClassVar[Kernel.State]
        STATE_STARTING: _ClassVar[Kernel.State]
        STATE_RUNNING_IDLE: _ClassVar[Kernel.State]
        STATE_RUNNING_BUSY: _ClassVar[Kernel.State]
    STATE_UNSPECIFIED: Kernel.State
    STATE_STARTING: Kernel.State
    STATE_RUNNING_IDLE: Kernel.State
    STATE_RUNNING_BUSY: Kernel.State
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNSPECIFIED: _ClassVar[Kernel.Type]
        TYPE_NOTEBOOK: _ClassVar[Kernel.Type]
        TYPE_ON_DEMAND: _ClassVar[Kernel.Type]
    TYPE_UNSPECIFIED: Kernel.Type
    TYPE_NOTEBOOK: Kernel.Type
    TYPE_ON_DEMAND: Kernel.Type
    class EnvironmentalVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_KERNEL_SPEC_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTAL_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    CREATOR_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TASK_FIELD_NUMBER: _ClassVar[int]
    CURRENT_TASK_SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TASK_QUEUE_SIZE_FIELD_NUMBER: _ClassVar[int]
    LAST_ACTIVITY_TIME_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    display_name: str
    image: str
    template: str
    notebook_kernel_spec: str
    environmental_variables: _containers.ScalarMap[str, str]
    creator: str
    creator_display_name: str
    state: Kernel.State
    type: Kernel.Type
    current_task: str
    current_task_sequence_number: int
    task_queue_size: int
    last_activity_time: _timestamp_pb2.Timestamp
    create_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., display_name: _Optional[str] = ..., image: _Optional[str] = ..., template: _Optional[str] = ..., notebook_kernel_spec: _Optional[str] = ..., environmental_variables: _Optional[_Mapping[str, str]] = ..., creator: _Optional[str] = ..., creator_display_name: _Optional[str] = ..., state: _Optional[_Union[Kernel.State, str]] = ..., type: _Optional[_Union[Kernel.Type, str]] = ..., current_task: _Optional[str] = ..., current_task_sequence_number: _Optional[int] = ..., task_queue_size: _Optional[int] = ..., last_activity_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
