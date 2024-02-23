import pprint

from h2o_notebook.gen.model.v1_notebook_kernel_spec import V1NotebookKernelSpec


class NotebookKernelSpec:
    def __init__(self,
                 name: str,
                 kernel_image: str,
                 kernel_template: str,
                 display_name: str = "",
                 disabled: bool = False):
        self.name = name
        self.kernel_image = kernel_image
        self.kernel_template = kernel_template
        self.display_name = display_name
        self.disabled = disabled

        self.notebook_kernel_spec_id = ""
        if name:
            self.notebook_kernel_spec_id = self.name.split("/")[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def to_api_object(self) -> V1NotebookKernelSpec:
        return V1NotebookKernelSpec(
            display_name=self.display_name,
            kernel_image=self.kernel_image,
            kernel_template=self.kernel_template,
            disabled=self.disabled,
        )


def from_api_object(api_object: V1NotebookKernelSpec) -> NotebookKernelSpec:
    return NotebookKernelSpec(
        name=api_object.name,
        kernel_image=api_object.kernel_image,
        kernel_template=api_object.kernel_template,
        display_name=api_object.display_name,
        disabled=api_object.disabled,
    )
