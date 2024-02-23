from typing import List
from typing import Optional

from h2o_notebook.clients.auth.token_api_client import TokenApiClient
from h2o_notebook.clients.connection_config import ConnectionConfig
from h2o_notebook.clients.kernel_image.client import KernelImageClient
from h2o_notebook.clients.kernel_image.kernel_image_config import KernelImageConfig
from h2o_notebook.clients.kernel_template.client import KernelTemplateClient
from h2o_notebook.clients.kernel_template.kernel_template_config import (
    KernelTemplateConfig,
)
from h2o_notebook.clients.notebook_kernel_spec.notebook_kernel_spec import (
    NotebookKernelSpec,
)
from h2o_notebook.clients.notebook_kernel_spec.notebook_kernel_spec import (
    from_api_object,
)
from h2o_notebook.clients.notebook_kernel_spec.notebook_kernel_spec_config import (
    NotebookKernelSpecConfig,
)
from h2o_notebook.clients.notebook_kernel_spec.page import NotebookKernelSpecsPage
from h2o_notebook.exception import CustomApiException
from h2o_notebook.gen import ApiException
from h2o_notebook.gen import Configuration
from h2o_notebook.gen.api.notebook_kernel_spec_service_api import (
    NotebookKernelSpecServiceApi,
)
from h2o_notebook.gen.model.v1_list_notebook_kernel_specs_response import (
    V1ListNotebookKernelSpecsResponse,
)
from h2o_notebook.gen.model.v1_notebook_kernel_spec import V1NotebookKernelSpec


class NotebookKernelSpecClient:
    """NotebookKernelSpecClient manages notebook kernel specs."""

    def __init__(
            self,
            connection_config: ConnectionConfig,
            verify_ssl: bool = True,
            ssl_ca_cert: Optional[str] = None,
            kernel_image_client: KernelImageClient = None,
            kernel_template_client: KernelTemplateClient = None,
    ):
        configuration = Configuration(host=connection_config.server_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        self.kernel_image_client = kernel_image_client
        self.kernel_template_client = kernel_template_client

        with TokenApiClient(
                configuration, connection_config.token_provider
        ) as api_client:
            self.api_instance = NotebookKernelSpecServiceApi(api_client)

    def create_notebook_kernel_spec(
            self,
            notebook_kernel_spec_id: str,
            kernel_image_id: str,
            kernel_template_id: str,
            disabled: bool = False,
            display_name: str = "",
    ) -> NotebookKernelSpec:
        """Creates a NotebookKernelSpec.

        Args:
            notebook_kernel_spec_id (str): The ID to use for the NotebookKernelSpec, which will become the final component of the spec's resource name.
                This value must:

                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character

            kernel_image_id (str): ID of a KernelImage resource.
            kernel_template_id (str): ID of a KernelTemplate resource.
            disabled (bool): Whether spec is disabled.
            display_name (str, optional): Human-readable name of the NotebookKernelSpec. Must contain at most 63 characters. Does not have to be unique.

        Returns:
            NotebookKernelSpec: NotebookKernelSpec object.
        """
        api_object = V1NotebookKernelSpec(
            kernel_image=KernelImageClient.build_resource_name(resource_id=kernel_image_id),
            kernel_template=KernelTemplateClient.build_resource_name(resource_id=kernel_template_id),
            display_name=display_name,
            disabled=disabled,
        )
        created_api_object: V1NotebookKernelSpec

        try:
            created_api_object = self.api_instance.notebook_kernel_spec_service_create_notebook_kernel_spec(
                notebook_kernel_spec=api_object, notebook_kernel_spec_id=notebook_kernel_spec_id
            ).notebook_kernel_spec
        except ApiException as e:
            raise CustomApiException(e)
        print(created_api_object)
        return from_api_object(api_object=created_api_object)

    def get_notebook_kernel_spec(self, notebook_kernel_spec_id: str) -> NotebookKernelSpec:
        """Returns a NotebookKernelSpec.

        Args:
            notebook_kernel_spec_id (str): NotebookKernelSpec ID.

        Returns:
            NotebookKernelSpec: NotebookKernelSpec object.
        """
        api_object: V1NotebookKernelSpec

        try:
            api_object = self.api_instance.notebook_kernel_spec_service_get_notebook_kernel_spec(
                name_4=self.build_resource_name(resource_id=notebook_kernel_spec_id)
            ).notebook_kernel_spec
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_notebook_kernel_specs(
            self,
            page_size: int = 0,
            page_token: str = "",
    ) -> NotebookKernelSpecsPage:
        """Lists NotebookKernelSpecs.

        Args:
            page_size (int): Maximum number of NotebookKernelSpecs to return in a response.
                If unspecified (or set to 0), at most 50 NotebookKernelSpecs will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the NotebookKernelSpecsPage.

        Returns:
            NotebookKernelSpecsPage: NotebookKernelSpecsPage object.
        """
        list_response: V1ListNotebookKernelSpecsResponse

        try:
            list_response = (
                self.api_instance.notebook_kernel_spec_service_list_notebook_kernel_specs(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return NotebookKernelSpecsPage(list_response)

    def list_all_notebook_kernel_specs(self) -> List[NotebookKernelSpec]:
        """ List all NotebookKernelSpecs.
        Returns:
            List of NotebookKernelSpec.
        """
        all_notebook_kernel_specs: List[NotebookKernelSpec] = []
        next_page_token = ""
        while True:
            notebook_kernel_spec_list = self.list_notebook_kernel_specs(
                page_size=0,
                page_token=next_page_token,
            )
            all_notebook_kernel_specs = all_notebook_kernel_specs + notebook_kernel_spec_list.notebook_kernel_specs
            next_page_token = notebook_kernel_spec_list.next_page_token
            if next_page_token == "":
                break

        return all_notebook_kernel_specs

    def apply_notebook_kernel_specs(self, notebook_kernel_spec_configs: List[NotebookKernelSpecConfig]) -> List[NotebookKernelSpec]:

        self.delete_all_notebook_kernel_specs()

        for cfg in notebook_kernel_spec_configs:
            self.create_notebook_kernel_spec(
                notebook_kernel_spec_id=cfg.notebook_kernel_spec_id,
                kernel_image_id=cfg.kernel_image_id,
                kernel_template_id=cfg.kernel_template_id,
                display_name=cfg.display_name,
                disabled=cfg.disabled,
            )

        return self.list_all_notebook_kernel_specs()

    def apply_kernel_images_templates_notebook_specs(
            self,
            kernel_image_configs: List[KernelImageConfig],
            kernel_template_configs: List[KernelTemplateConfig],
            notebook_kernel_spec_configs: List[NotebookKernelSpecConfig],
    ) -> List[NotebookKernelSpec]:
        """
        Set all KernelImages, KernelTemplates and NotebookKernelSpecs to a state defined in the arguments.
        Objects not specified in the arguments will be deleted.
        Objects specified in the arguments will be recreated with the new values.

        Args:
            kernel_image_configs: configuration of KernelImages that should be applied.
            kernel_template_configs: configuration of KernelTemplates that should be applied.
            notebook_kernel_spec_configs: configuration of NotebookKernelSpecs that should be applied.
        Returns: applied NotebookKernelSpecs
        """
        self.delete_all_notebook_kernel_specs()
        self.kernel_image_client.delete_all_kernel_images()
        self.kernel_template_client.delete_all_kernel_templates()

        self.kernel_image_client.apply_kernel_images(kernel_image_configs)
        self.kernel_template_client.apply_kernel_templates(kernel_template_configs)

        for cfg in notebook_kernel_spec_configs:
            self.create_notebook_kernel_spec(
                notebook_kernel_spec_id=cfg.notebook_kernel_spec_id,
                kernel_image_id=cfg.kernel_image_id,
                kernel_template_id=cfg.kernel_template_id,
                display_name=cfg.display_name,
                disabled=cfg.disabled,
            )

        return self.list_all_notebook_kernel_specs()

    def delete_notebook_kernel_spec(self, notebook_kernel_spec_id: str) -> None:
        """Deletes a NotebookKernelSpec.

        Args:
            notebook_kernel_spec_id (str): NotebookKernelSpec ID.
        """
        try:
            self.api_instance.notebook_kernel_spec_service_delete_notebook_kernel_spec(
                name_3=self.build_resource_name(resource_id=notebook_kernel_spec_id)
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_notebook_kernel_specs(self) -> None:
        """Helper function for deleting all NotebookKernelSpecs.
        """
        for n in self.list_all_notebook_kernel_specs():
            self.delete_notebook_kernel_spec(notebook_kernel_spec_id=n.notebook_kernel_spec_id)

    @staticmethod
    def build_resource_name(resource_id: str) -> str:
        """Helper function for building resource name."""
        return f"notebookKernelSpecs/{resource_id}"
