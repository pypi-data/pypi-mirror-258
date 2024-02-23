import pprint

from h2o_notebook.clients.kernel_image.type import KernelImageType


class KernelImageConfig:
    """KernelImageConfig object used as input for apply method."""

    def __init__(
            self,
            kernel_image_id: str,
            kernel_image_type: KernelImageType,
            image: str,
            display_name: str,
            disabled: bool,
    ):
        self.kernel_image_id = kernel_image_id
        self.display_name = display_name
        self.kernel_image_type = kernel_image_type
        self.image = image
        self.disabled = disabled

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
