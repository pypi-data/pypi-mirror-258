import pprint

from h2o_notebook.clients.kernel_image.type import KernelImageType
from h2o_notebook.gen.model.v1_kernel_image import V1KernelImage


class KernelImage:
    def __init__(self,
                 name: str,
                 kernel_image_type: KernelImageType,
                 image: str,
                 display_name: str,
                 disabled: bool):
        self.name = name
        self.kernel_image_type = kernel_image_type
        self.image = image
        self.display_name = display_name
        self.disabled = disabled

        self.kernel_image_id = ""
        if name:
            self.kernel_image_id = self.name.split("/")[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def to_api_object(self) -> V1KernelImage:
        return V1KernelImage(
            display_name=self.display_name,
            type=self.kernel_image_type.to_api_object(),
            image=self.image,
            disabled=self.disabled,
        )


def from_api_object(api_object: V1KernelImage) -> KernelImage:
    return KernelImage(
        name=api_object.name,
        kernel_image_type=KernelImageType(str(api_object.type)),
        image=api_object.image,
        display_name=api_object.display_name,
        disabled=api_object.disabled,
    )
