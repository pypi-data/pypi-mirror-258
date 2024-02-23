from h2o_notebook.gen.ai.h2o.notebook.v1 import kernel_pb2 as _kernel_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import resource_pb2 as _resource_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateKernelRequest(_message.Message):
    __slots__ = ("kernel", "kernel_id")
    KERNEL_FIELD_NUMBER: _ClassVar[int]
    KERNEL_ID_FIELD_NUMBER: _ClassVar[int]
    kernel: _kernel_pb2.Kernel
    kernel_id: str
    def __init__(self, kernel: _Optional[_Union[_kernel_pb2.Kernel, _Mapping]] = ..., kernel_id: _Optional[str] = ...) -> None: ...

class CreateKernelResponse(_message.Message):
    __slots__ = ("kernel",)
    KERNEL_FIELD_NUMBER: _ClassVar[int]
    kernel: _kernel_pb2.Kernel
    def __init__(self, kernel: _Optional[_Union[_kernel_pb2.Kernel, _Mapping]] = ...) -> None: ...

class GetKernelRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetKernelResponse(_message.Message):
    __slots__ = ("kernel",)
    KERNEL_FIELD_NUMBER: _ClassVar[int]
    kernel: _kernel_pb2.Kernel
    def __init__(self, kernel: _Optional[_Union[_kernel_pb2.Kernel, _Mapping]] = ...) -> None: ...

class ListKernelsRequest(_message.Message):
    __slots__ = ("page_size", "page_token", "order_by", "filter")
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    page_size: int
    page_token: str
    order_by: str
    filter: str
    def __init__(self, page_size: _Optional[int] = ..., page_token: _Optional[str] = ..., order_by: _Optional[str] = ..., filter: _Optional[str] = ...) -> None: ...

class ListKernelsResponse(_message.Message):
    __slots__ = ("kernels", "next_page_token", "total_size")
    KERNELS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    kernels: _containers.RepeatedCompositeFieldContainer[_kernel_pb2.Kernel]
    next_page_token: str
    total_size: int
    def __init__(self, kernels: _Optional[_Iterable[_Union[_kernel_pb2.Kernel, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class DeleteKernelRequest(_message.Message):
    __slots__ = ("name", "allow_missing", "validate_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MISSING_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    allow_missing: bool
    validate_only: bool
    def __init__(self, name: _Optional[str] = ..., allow_missing: bool = ..., validate_only: bool = ...) -> None: ...

class DeleteKernelResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class InterruptKernelRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class InterruptKernelResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
