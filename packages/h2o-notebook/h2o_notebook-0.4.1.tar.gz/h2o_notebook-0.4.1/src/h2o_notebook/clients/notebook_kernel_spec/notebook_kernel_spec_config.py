import pprint


class NotebookKernelSpecConfig:
    """NotebookKernelSpecConfig object used as input for apply method."""

    def __init__(
            self,
            notebook_kernel_spec_id: str,
            kernel_image_id: str,
            kernel_template_id: str,
            display_name: str = "",
            disabled: bool = False,
    ):
        self.notebook_kernel_spec_id = notebook_kernel_spec_id
        self.kernel_image_id = kernel_image_id
        self.kernel_template_id = kernel_template_id
        self.display_name = display_name
        self.disabled = disabled

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
