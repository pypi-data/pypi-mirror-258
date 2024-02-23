from h2o_notebook.gen.ai.h2o.notebook.v1 import kernel_image_pb2 as _kernel_image_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.api import resource_pb2 as _resource_pb2
from google.api import client_pb2 as _client_pb2
from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateKernelImageRequest(_message.Message):
    __slots__ = ("kernel_image", "kernel_image_id")
    KERNEL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    KERNEL_IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
    kernel_image: _kernel_image_pb2.KernelImage
    kernel_image_id: str
    def __init__(self, kernel_image: _Optional[_Union[_kernel_image_pb2.KernelImage, _Mapping]] = ..., kernel_image_id: _Optional[str] = ...) -> None: ...

class CreateKernelImageResponse(_message.Message):
    __slots__ = ("kernel_image",)
    KERNEL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    kernel_image: _kernel_image_pb2.KernelImage
    def __init__(self, kernel_image: _Optional[_Union[_kernel_image_pb2.KernelImage, _Mapping]] = ...) -> None: ...

class GetKernelImageRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetKernelImageResponse(_message.Message):
    __slots__ = ("kernel_image",)
    KERNEL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    kernel_image: _kernel_image_pb2.KernelImage
    def __init__(self, kernel_image: _Optional[_Union[_kernel_image_pb2.KernelImage, _Mapping]] = ...) -> None: ...

class ListKernelImagesRequest(_message.Message):
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

class ListKernelImagesResponse(_message.Message):
    __slots__ = ("kernel_images", "next_page_token", "total_size")
    KERNEL_IMAGES_FIELD_NUMBER: _ClassVar[int]
    NEXT_PAGE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    kernel_images: _containers.RepeatedCompositeFieldContainer[_kernel_image_pb2.KernelImage]
    next_page_token: str
    total_size: int
    def __init__(self, kernel_images: _Optional[_Iterable[_Union[_kernel_image_pb2.KernelImage, _Mapping]]] = ..., next_page_token: _Optional[str] = ..., total_size: _Optional[int] = ...) -> None: ...

class UpdateKernelImageRequest(_message.Message):
    __slots__ = ("kernel_image", "update_mask", "allow_missing", "validate_only")
    KERNEL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MISSING_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    kernel_image: _kernel_image_pb2.KernelImage
    update_mask: _field_mask_pb2.FieldMask
    allow_missing: bool
    validate_only: bool
    def __init__(self, kernel_image: _Optional[_Union[_kernel_image_pb2.KernelImage, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., allow_missing: bool = ..., validate_only: bool = ...) -> None: ...

class UpdateKernelImageResponse(_message.Message):
    __slots__ = ("kernel_image",)
    KERNEL_IMAGE_FIELD_NUMBER: _ClassVar[int]
    kernel_image: _kernel_image_pb2.KernelImage
    def __init__(self, kernel_image: _Optional[_Union[_kernel_image_pb2.KernelImage, _Mapping]] = ...) -> None: ...

class DeleteKernelImageRequest(_message.Message):
    __slots__ = ("name", "allow_missing", "validate_only")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MISSING_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_ONLY_FIELD_NUMBER: _ClassVar[int]
    name: str
    allow_missing: bool
    validate_only: bool
    def __init__(self, name: _Optional[str] = ..., allow_missing: bool = ..., validate_only: bool = ...) -> None: ...

class DeleteKernelImageResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
