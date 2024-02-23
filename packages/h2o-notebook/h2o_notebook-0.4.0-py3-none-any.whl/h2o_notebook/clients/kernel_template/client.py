from typing import Dict
from typing import List
from typing import Optional

from h2o_notebook.clients.auth.token_api_client import TokenApiClient
from h2o_notebook.clients.connection_config import ConnectionConfig
from h2o_notebook.clients.convert.duration_convertor import duration_to_seconds
from h2o_notebook.clients.convert.quantity_convertor import quantity_to_number_str
from h2o_notebook.clients.kernel_template.kernel_template import KernelTemplate
from h2o_notebook.clients.kernel_template.kernel_template import from_api_object
from h2o_notebook.clients.kernel_template.kernel_template_config import (
    KernelTemplateConfig,
)
from h2o_notebook.clients.kernel_template.page import KernelTemplatesPage
from h2o_notebook.exception import CustomApiException
from h2o_notebook.gen import ApiException
from h2o_notebook.gen import Configuration
from h2o_notebook.gen.api.kernel_template_service_api import KernelTemplateServiceApi
from h2o_notebook.gen.model.v1_kernel_template import V1KernelTemplate
from h2o_notebook.gen.model.v1_list_kernel_templates_response import (
    V1ListKernelTemplatesResponse,
)


class KernelTemplateClient:
    """KernelTemplateClient manages Python kernel templates."""

    def __init__(
            self,
            connection_config: ConnectionConfig,
            verify_ssl: bool = True,
            ssl_ca_cert: Optional[str] = None,
    ):
        configuration = Configuration(host=connection_config.server_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
                configuration, connection_config.token_provider
        ) as api_client:
            self.api_instance = KernelTemplateServiceApi(api_client)

    def create_kernel_template(
            self,
            kernel_template_id: str,
            milli_cpu_limit: int,
            gpu: int,
            memory_bytes_limit: str,
            max_idle_duration: str,
            environmental_variables: Dict[str, str] = None,
            yaml_pod_template_spec: str = "",
            gpu_resource: str = "",
            milli_cpu_request: int = 0,
            memory_bytes_request: str = "0",
            disabled: bool = False,
    ) -> KernelTemplate:
        """Creates a KernelTemplate.

        Args:
            kernel_template_id (str): The ID to use for the KernelTemplate, which will become the final component of the template's resource name.
                This value must:

                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
            milli_cpu_limit (int): The maximum amount of CPU the KernelTemplate is allowed to use.
            gpu (int): The number of GPUs the KernelTemplate is allowed to use.
            memory_bytes_limit (str): The maximum amount of memory the KernelTemplate is allowed to use.
            max_idle_duration (str): The maximum amount of time the KernelTemplate is allowed to be idle. Must be specified as a number with `s` suffix. Example `3600s`.
            environmental_variables (Dict[str, str], optional): A set of key-value pairs that are passed to the KernelTemplate as environment variables.
            yaml_pod_template_spec (str, optional): The YAML pod template spec for the KernelTemplate.
            gpu_resource (str, optional): The name of the GPU resource the KernelTemplate is allowed to use. If not specified, a default value will be used.
            milli_cpu_request (int, optional): The minimum amount of CPU the KernelTemplate is allowed to use. If not specified, milli_cpu_limit value will be used.
            memory_bytes_request (str, optional): The minimum amount of memory the KernelTemplate is allowed to use. If not specified, memory_bytes_limit value will be used.
            disabled (bool): Whether template is disabled.

        Returns:
            KernelTemplate: KernelTemplate object.
        """
        if environmental_variables is None:
            environmental_variables = {}

        api_object = V1KernelTemplate(
            milli_cpu_limit=milli_cpu_limit,
            gpu=gpu,
            memory_bytes_limit=quantity_to_number_str(memory_bytes_limit),
            max_idle_duration=duration_to_seconds(max_idle_duration),
            environmental_variables=environmental_variables,
            yaml_pod_template_spec=yaml_pod_template_spec,
            gpu_resource=gpu_resource,
            milli_cpu_request=milli_cpu_request,
            memory_bytes_request=quantity_to_number_str(memory_bytes_request),
            disabled=disabled,
        )
        created_api_object: V1KernelTemplate

        try:
            created_api_object = self.api_instance.kernel_template_service_create_kernel_template(
                kernel_template=api_object, kernel_template_id=kernel_template_id
            ).kernel_template
        except ApiException as e:
            raise CustomApiException(e)
        print(created_api_object)
        return from_api_object(api_object=created_api_object)

    def get_kernel_template(self, kernel_template_id: str) -> KernelTemplate:
        """Returns a KernelTemplate.

        Args:
            kernel_template_id (str): KernelTemplate ID.

        Returns:
            KernelTemplate: KernelTemplate object.
        """
        api_object: V1KernelTemplate

        try:
            api_object = self.api_instance.kernel_template_service_get_kernel_template(
                name_3=self.build_resource_name(
                    resource_id=kernel_template_id,
                )
            ).kernel_template
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_kernel_templates(
            self,
            page_size: int = 0,
            page_token: str = "",
    ) -> KernelTemplatesPage:
        """Lists KernelTemplates.

        Args:
            page_size (int): Maximum number of KernelTemplates to return in a response.
                If unspecified (or set to 0), at most 50 KernelTemplates will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the KernelTemplatesPage.

        Returns:
            KernelTemplatesPage: KernelTemplatesPage object.
        """
        list_response: V1ListKernelTemplatesResponse

        try:
            list_response = (
                self.api_instance.kernel_template_service_list_kernel_templates(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return KernelTemplatesPage(list_response)

    def list_all_kernel_templates(self) -> List[KernelTemplate]:
        """ List all KernelTemplates.

        Returns:
            List of KernelTemplate.
        """
        all_kernel_templates: List[KernelTemplate] = []
        next_page_token = ""
        while True:
            kernel_template_list = self.list_kernel_templates(
                page_size=0,
                page_token=next_page_token,
            )
            all_kernel_templates = all_kernel_templates + kernel_template_list.kernel_templates
            next_page_token = kernel_template_list.next_page_token
            if next_page_token == "":
                break

        return all_kernel_templates

    def apply_kernel_templates(self, kernel_template_configs: List[KernelTemplateConfig]) -> List[KernelTemplate]:
        """
        Set all KernelTemplates to a state defined in kernel_template_configs.
        KernelTemplates not specified in the kernel_template_configs will be deleted.
        KernelTemplates specified in the kernel_template_configs will be recreated with the new values.

        Args:
            kernel_template_configs: configuration of KernelTemplates that should be applied.
        Returns: applied KernelTemplates
        """
        self.delete_all_kernel_templates()

        for cfg in kernel_template_configs:
            self.create_kernel_template(
                kernel_template_id=cfg.kernel_template_id,
                milli_cpu_limit=cfg.milli_cpu_limit,
                gpu=cfg.gpu,
                memory_bytes_limit=cfg.memory_bytes_limit,
                max_idle_duration=cfg.max_idle_duration,
                environmental_variables=cfg.environmental_variables,
                yaml_pod_template_spec=cfg.yaml_pod_template_spec,
                gpu_resource=cfg.gpu_resource,
                milli_cpu_request=cfg.milli_cpu_request,
                memory_bytes_request=cfg.memory_bytes_request,
                disabled=cfg.disabled,
            )

        return self.list_all_kernel_templates()

    def delete_kernel_template(self, kernel_template_id: str) -> None:
        """Deletes a KernelTemplate.

        Args:
            kernel_template_id (str): KernelTemplate ID.
        """
        try:
            self.api_instance.kernel_template_service_delete_kernel_template(
                name_2=self.build_resource_name(
                    resource_id=kernel_template_id,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_kernel_templates(self) -> None:
        """Helper function for deleting all KernelTemplates.
        """

        for n in self.list_all_kernel_templates():
            self.delete_kernel_template(kernel_template_id=n.kernel_template_id)

    @staticmethod
    def build_resource_name(resource_id: str) -> str:
        """Helper function for building resource name."""
        return f"kernelTemplates/{resource_id}"

