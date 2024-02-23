from google.api import resource_pb2 as _resource_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KernelTemplate(_message.Message):
    __slots__ = ("name", "milli_cpu_request", "milli_cpu_limit", "gpu_resource", "gpu", "memory_bytes_request", "memory_bytes_limit", "environmental_variables", "yaml_pod_template_spec", "disabled", "max_idle_duration", "create_time", "update_time")
    class EnvironmentalVariablesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    MILLI_CPU_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MILLI_CPU_LIMIT_FIELD_NUMBER: _ClassVar[int]
    GPU_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    GPU_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_REQUEST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_BYTES_LIMIT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTAL_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    YAML_POD_TEMPLATE_SPEC_FIELD_NUMBER: _ClassVar[int]
    DISABLED_FIELD_NUMBER: _ClassVar[int]
    MAX_IDLE_DURATION_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    milli_cpu_request: int
    milli_cpu_limit: int
    gpu_resource: str
    gpu: int
    memory_bytes_request: int
    memory_bytes_limit: int
    environmental_variables: _containers.ScalarMap[str, str]
    yaml_pod_template_spec: str
    disabled: bool
    max_idle_duration: _duration_pb2.Duration
    create_time: _timestamp_pb2.Timestamp
    update_time: _timestamp_pb2.Timestamp
    def __init__(self, name: _Optional[str] = ..., milli_cpu_request: _Optional[int] = ..., milli_cpu_limit: _Optional[int] = ..., gpu_resource: _Optional[str] = ..., gpu: _Optional[int] = ..., memory_bytes_request: _Optional[int] = ..., memory_bytes_limit: _Optional[int] = ..., environmental_variables: _Optional[_Mapping[str, str]] = ..., yaml_pod_template_spec: _Optional[str] = ..., disabled: bool = ..., max_idle_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., update_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
