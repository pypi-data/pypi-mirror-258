from google.api import resource_pb2 as _resource_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KernelTask(_message.Message):
    __slots__ = ("name", "code", "state", "sequence_number", "tasks_ahead_count", "stdout", "error", "error_value", "traceback", "create_time", "execution_start_time", "complete_time")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATE_UNSPECIFIED: _ClassVar[KernelTask.State]
        STATE_QUEUED: _ClassVar[KernelTask.State]
        STATE_EXECUTING: _ClassVar[KernelTask.State]
        STATE_COMPLETE_ERROR: _ClassVar[KernelTask.State]
        STATE_COMPLETE_SUCCESS: _ClassVar[KernelTask.State]
    STATE_UNSPECIFIED: KernelTask.State
    STATE_QUEUED: KernelTask.State
    STATE_EXECUTING: KernelTask.State
    STATE_COMPLETE_ERROR: KernelTask.State
    STATE_COMPLETE_SUCCESS: KernelTask.State
    NAME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TASKS_AHEAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    STDOUT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_VALUE_FIELD_NUMBER: _ClassVar[int]
    TRACEBACK_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_START_TIME_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    code: str
    state: KernelTask.State
    sequence_number: int
    tasks_ahead_count: int
    stdout: str
    error: str
    error_value: str
    traceback: str
    create_time: _timestamp_pb2.Timestamp
    execution_start_time: _timestamp_pb2.Timestamp
    complete_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., code: _Optional[str] = ..., state: _Optional[_Union[KernelTask.State, str]] = ..., sequence_number: _Optional[int] = ..., tasks_ahead_count: _Optional[int] = ..., stdout: _Optional[str] = ..., error: _Optional[str] = ..., error_value: _Optional[str] = ..., traceback: _Optional[str] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., execution_start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., complete_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
