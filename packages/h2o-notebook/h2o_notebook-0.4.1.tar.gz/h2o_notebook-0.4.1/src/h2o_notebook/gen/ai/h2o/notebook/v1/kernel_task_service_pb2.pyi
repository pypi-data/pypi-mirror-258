from h2o_notebook.gen.ai.h2o.notebook.v1 import kernel_task_pb2 as _kernel_task_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import resource_pb2 as _resource_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateKernelTaskRequest(_message.Message):
    __slots__ = ("parent", "kernel_task", "kernel_task_id")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    KERNEL_TASK_FIELD_NUMBER: _ClassVar[int]
    KERNEL_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    parent: str
    kernel_task: _kernel_task_pb2.KernelTask
    kernel_task_id: str
    def __init__(self, parent: _Optional[str] = ..., kernel_task: _Optional[_Union[_kernel_task_pb2.KernelTask, _Mapping]] = ..., kernel_task_id: _Optional[str] = ...) -> None: ...

class CreateKernelTaskResponse(_message.Message):
    __slots__ = ("kernel_task",)
    KERNEL_TASK_FIELD_NUMBER: _ClassVar[int]
    kernel_task: _kernel_task_pb2.KernelTask
    def __init__(self, kernel_task: _Optional[_Union[_kernel_task_pb2.KernelTask, _Mapping]] = ...) -> None: ...

class GetKernelTaskRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetKernelTaskResponse(_message.Message):
    __slots__ = ("kernel_task",)
    KERNEL_TASK_FIELD_NUMBER: _ClassVar[int]
    kernel_task: _kernel_task_pb2.KernelTask
    def __init__(self, kernel_task: _Optional[_Union[_kernel_task_pb2.KernelTask, _Mapping]] = ...) -> None: ...

class ListKernelTasksRequest(_message.Message):
    __slots__ = ("parent", "page_size", "page_token", "order_by", "filter")
    PARENT_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    parent: str
    page_size: int
    page_token: str
    order_by: str
    filter: str
    def __init__(self, parent: _Optional[str] = ..., page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., order_by: _Optional[str] = ..., filter: _Optional[str] = ...) -> None: ...

class ListKernelTasksResponse(_message.Message):
    __slots__ = ("kernel_tasks", "next_page_token", "total_size")
    KERNEL_TASKS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    kernel_tasks: _containers.RepeatedCompositeFieldContainer[_kernel_task_pb2.KernelTask]
    next_page_token: str
    total_size: int
    def __init__(self, kernel_tasks: _Optional[_Iterable[_Union[_kernel_task_pb2.KernelTask, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...
