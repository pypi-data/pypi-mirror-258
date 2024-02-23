from typing import List
from typing import Optional

from h2o_notebook.clients.auth.token_api_client import TokenApiClient
from h2o_notebook.clients.connection_config import ConnectionConfig
from h2o_notebook.clients.kernel_image.kernel_image import KernelImage
from h2o_notebook.clients.kernel_image.kernel_image import from_api_object
from h2o_notebook.clients.kernel_image.kernel_image_config import KernelImageConfig
from h2o_notebook.clients.kernel_image.page import KernelImagesPage
from h2o_notebook.clients.kernel_image.type import KernelImageType
from h2o_notebook.exception import CustomApiException
from h2o_notebook.gen import ApiException
from h2o_notebook.gen import Configuration
from h2o_notebook.gen.api.kernel_image_service_api import KernelImageServiceApi
from h2o_notebook.gen.model.v1_kernel_image import V1KernelImage
from h2o_notebook.gen.model.v1_list_kernel_images_response import (
    V1ListKernelImagesResponse,
)


class KernelImageClient:
    """KernelImageClient manages Python kernel images."""

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
            self.api_instance = KernelImageServiceApi(api_client)

    def create_kernel_image(
            self,
            kernel_image_id: str,
            kernel_image_type: KernelImageType,
            image: str,
            disabled: bool = False,
            display_name: str = "",
    ) -> KernelImage:
        """Creates a KernelImage.

        Args:
            kernel_image_id (str): The ID to use for the KernelImage, which will become the final component of the image's resource name.
                This value must:

                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
            kernel_image_type (KernelImageType): KernelImage type.
            image (str): Docker image.
            disabled (bool): Whether image is disabled.
            display_name (str, optional): Human-readable name of the KernelImage. Must contain at most 63 characters. Does not have to be unique.

        Returns:
            KernelImage: KernelImage object.
        """
        api_object = V1KernelImage(
            type=kernel_image_type.to_api_object(),
            image=image,
            display_name=display_name,
            disabled=disabled,
        )
        created_api_object: V1KernelImage

        try:
            created_api_object = self.api_instance.kernel_image_service_create_kernel_image(
                kernel_image=api_object, kernel_image_id=kernel_image_id
            ).kernel_image
        except ApiException as e:
            raise CustomApiException(e)
        print(created_api_object)
        return from_api_object(api_object=created_api_object)

    def get_kernel_image(self, kernel_image_id: str) -> KernelImage:
        """Returns a KernelImage.

        Args:
            kernel_image_id (str): KernelImage ID.

        Returns:
            KernelImage: KernelImage object.
        """
        api_object: V1KernelImage

        try:
            api_object = self.api_instance.kernel_image_service_get_kernel_image(
                name=self.build_resource_name(resource_id=kernel_image_id)
            ).kernel_image
        except ApiException as e:
            raise CustomApiException(e)

        return from_api_object(api_object=api_object)

    def list_kernel_images(
            self,
            page_size: int = 0,
            page_token: str = "",
    ) -> KernelImagesPage:
        """Lists KernelImages.

        Args:
            page_size (int): Maximum number of KernelImages to return in a response.
                If unspecified (or set to 0), at most 50 KernelImages will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str): Page token.
                Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the KernelImagesPage.

        Returns:
            KernelImagesPage: KernelImagesPage object.
        """
        list_response: V1ListKernelImagesResponse

        try:
            list_response = (
                self.api_instance.kernel_image_service_list_kernel_images(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except ApiException as e:
            raise CustomApiException(e)

        return KernelImagesPage(list_response)

    def list_all_kernel_images(self) -> List[KernelImage]:
        """ List all KernelImages.
        Returns:
            List of KernelImage.
        """
        all_kernel_images: List[KernelImage] = []
        next_page_token = ""
        while True:
            kernel_image_list = self.list_kernel_images(
                page_size=0,
                page_token=next_page_token,
            )
            all_kernel_images = all_kernel_images + kernel_image_list.kernel_images
            next_page_token = kernel_image_list.next_page_token
            if next_page_token == "":
                break

        return all_kernel_images

    def apply_kernel_images(self, kernel_image_configs: List[KernelImageConfig]) -> List[KernelImage]:
        """
        Set all KernelImages to a state defined in kernel_image_configs.
        KernelImages not specified in the kernel_image_configs will be deleted.
        KernelImages specified in the kernel_image_configs will be recreated with the new values.

        Args:
            kernel_image_configs: configuration of KernelImages that should be applied.
        Returns: applied KernelImages
        """
        self.delete_all_kernel_images()

        for cfg in kernel_image_configs:
            self.create_kernel_image(
                kernel_image_id=cfg.kernel_image_id,
                kernel_image_type=cfg.kernel_image_type,
                image=cfg.image,
                display_name=cfg.display_name,
                disabled=cfg.disabled,
            )

        return self.list_all_kernel_images()

    def delete_kernel_image(self, kernel_image_id: str) -> None:
        """Deletes a KernelImage.

        Args:
            kernel_image_id (str): KernelImage ID.
        """
        try:
            self.api_instance.kernel_image_service_delete_kernel_image(
                name=self.build_resource_name(resource_id=kernel_image_id)
            )
        except ApiException as e:
            raise CustomApiException(e)

    def delete_all_kernel_images(self) -> None:
        """Helper function for deleting all KernelImages.
        """
        for n in self.list_all_kernel_images():
            self.delete_kernel_image(kernel_image_id=n.kernel_image_id)

    @staticmethod
    def build_resource_name(resource_id: str) -> str:
        """Helper function for building resource name."""
        return f"kernelImages/{resource_id}"
