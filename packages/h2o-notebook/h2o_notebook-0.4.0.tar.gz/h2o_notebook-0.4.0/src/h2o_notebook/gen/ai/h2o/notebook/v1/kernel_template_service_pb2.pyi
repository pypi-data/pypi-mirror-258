from h2o_notebook.gen.ai.h2o.notebook.v1 import kernel_template_pb2 as _kernel_template_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import resource_pb2 as _resource_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateKernelTemplateRequest(_message.Message):
    __slots__ = ("kernel_template", "kernel_template_id")
    KERNEL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    KERNEL_TEMPLATE_ID_FIELD_NUMBER: _ClassVar[int]
    kernel_template: _kernel_template_pb2.KernelTemplate
    kernel_template_id: str
    def __init__(self, kernel_template: _Optional[_Union[_kernel_template_pb2.KernelTemplate, _Mapping]] = ..., kernel_template_id: _Optional[str] = ...) -> None: ...

class CreateKernelTemplateResponse(_message.Message):
    __slots__ = ("kernel_template",)
    KERNEL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    kernel_template: _kernel_template_pb2.KernelTemplate
    def __init__(self, kernel_template: _Optional[_Union[_kernel_template_pb2.KernelTemplate, _Mapping]] = ...) -> None: ...

class GetKernelTemplateRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetKernelTemplateResponse(_message.Message):
    __slots__ = ("kernel_template",)
    KERNEL_TEMPLATE_FIELD_NUMBER: _ClassVar[int]
    kernel_template: _kernel_template_pb2.KernelTemplate
    def __init__(self, kernel_template: _Optional[_Union[_kernel_template_pb2.KernelTemplate, _Mapping]] = ...) -> None: ...

class ListKernelTemplatesRequest(_message.Message):
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

class ListKernelTemplatesResponse(_message.Message):
    __slots__ = ("kernel_templates", "next_page_token", "total_size")
    KERNEL_TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    kernel_templates: _containers.RepeatedCompositeFieldContainer[_kernel_template_pb2.KernelTemplate]
    next_page_token: str
    total_size: int
    def __init__(self, kernel_templates: _Optional[_Iterable[_Union[_kernel_template_pb2.KernelTemplate, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class DeleteKernelTemplateRequest(_message.Message):
    __slots__ = ("name", "allow_missing", "validate_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MISSING_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    allow_missing: bool
    validate_only: bool
    def __init__(self, name: _Optional[str] = ..., allow_missing: bool = ..., validate_only: bool = ...) -> None: ...

class DeleteKernelTemplateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
