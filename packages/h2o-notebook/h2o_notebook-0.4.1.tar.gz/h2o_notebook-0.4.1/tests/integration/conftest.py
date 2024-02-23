import os
from typing import Tuple

import h2o_authn
import pytest as pytest
from h2o_authn import TokenProvider

import h2o_notebook
from h2o_notebook.clients.kernel_image.client import KernelImageClient
from h2o_notebook.clients.kernel_image.type import KernelImageType
from h2o_notebook.clients.kernel_template.client import KernelTemplateClient
from h2o_notebook.clients.notebook_kernel_spec.client import NotebookKernelSpecClient


@pytest.fixture(scope="session")
def session():
    return h2o_notebook.Session()


@pytest.fixture(scope="session")
def user_clients():
    return h2o_notebook.login_custom(
        endpoint=os.getenv("NOTEBOOK_SERVER_URL"),
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def super_admin_clients():
    return h2o_notebook.login_custom(
        endpoint=os.getenv("NOTEBOOK_SERVER_URL"),
        refresh_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def token_provider_user() -> TokenProvider:
    return h2o_authn.TokenProvider(
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def token_provider_super_admin() -> TokenProvider:
    return h2o_authn.TokenProvider(
        refresh_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def kernel_image_client_user(user_clients):
    return user_clients.kernel_image_client


@pytest.fixture(scope="session")
def kernel_image_client_super_admin(super_admin_clients):
    return super_admin_clients.kernel_image_client


@pytest.fixture(scope="function")
def delete_all_kernel_images_after(kernel_image_client_super_admin):
    yield
    kernel_image_client_super_admin.delete_all_kernel_images()


@pytest.fixture(scope="function")
def delete_all_kernel_images_before_after(kernel_image_client_super_admin):
    kernel_image_client_super_admin.delete_all_kernel_images()
    yield
    kernel_image_client_super_admin.delete_all_kernel_images()


@pytest.fixture(scope="function")
def kernel_image_super_admin(kernel_image_client_super_admin):
    ki = kernel_image_client_super_admin.create_kernel_image(
        kernel_image_id="kernel-image-super-admin",
        kernel_image_type=KernelImageType.TYPE_PYTHON,
        image="something",
    )
    yield ki
    kernel_image_client_super_admin.delete_kernel_image(kernel_image_id=ki.kernel_image_id)


@pytest.fixture(scope="session")
def kernel_template_client_user(user_clients):
    return user_clients.kernel_template_client


@pytest.fixture(scope="session")
def kernel_template_client_super_admin(super_admin_clients):
    return super_admin_clients.kernel_template_client


@pytest.fixture(scope="function")
def delete_all_kernel_templates_after(kernel_template_client_super_admin):
    yield
    kernel_template_client_super_admin.delete_all_kernel_templates()


@pytest.fixture(scope="function")
def kernel_template_super_admin(kernel_template_client_super_admin):
    kernel_template = kernel_template_client_super_admin.create_kernel_template(
        kernel_template_id="kernel-template-super-admin",
        milli_cpu_limit=200,
        milli_cpu_request=200,
        gpu=1,
        memory_bytes_limit="1M",
        memory_bytes_request="1M",
        max_idle_duration="1h",
    )
    yield kernel_template
    kernel_template_client_super_admin.delete_kernel_template(kernel_template_id=kernel_template.kernel_template_id)


@pytest.fixture(scope="function")
def kernel_template_user(kernel_template_client_user, kernel_template_client_super_admin):
    kernel_template = kernel_template_client_user.create_kernel_template(
        kernel_template_id="kernel-template-user",
        milli_cpu_limit=200,
        milli_cpu_request=200,
        gpu=1,
        memory_bytes_limit="1M",
        memory_bytes_request="1M",
        max_idle_duration="1h",
    )
    yield kernel_template
    kernel_template_client_super_admin.delete_kernel_template(kernel_template_id=kernel_template.kernel_template_id)


@pytest.fixture(scope="session")
def notebook_kernel_spec_client_user(user_clients):
    return user_clients.notebook_kernel_spec_client


@pytest.fixture(scope="session")
def notebook_kernel_spec_client_super_admin(super_admin_clients):
    return super_admin_clients.notebook_kernel_spec_client


@pytest.fixture(scope="function")
def notebook_kernel_spec_setup(
    kernel_image_client_super_admin: KernelImageClient,
    kernel_template_client_super_admin: KernelTemplateClient,
) -> Tuple[str, str]:
    kernel_image_id = "img1"
    kernel_template_id = "kt1"

    kernel_image_client_super_admin.create_kernel_image(
        kernel_image_id=kernel_image_id,
        kernel_image_type=KernelImageType.TYPE_PYTHON,
        image="something",
    )
    kernel_template_client_super_admin.create_kernel_template(
        kernel_template_id=kernel_template_id,
        milli_cpu_limit=200,
        gpu=1,
        memory_bytes_limit="1000",
        max_idle_duration="600s",
    )

    return kernel_image_id, kernel_template_id


@pytest.fixture(scope="function")
def kernel_image(kernel_image_client_super_admin: KernelImageClient):
    kernel_image = kernel_image_client_super_admin.create_kernel_image(
        kernel_image_id="img1",
        kernel_image_type=KernelImageType.TYPE_PYTHON,
        image="something",
    )

    yield kernel_image
    kernel_image_client_super_admin.delete_kernel_image(kernel_image_id=kernel_image.kernel_image_id)


@pytest.fixture(scope="function")
def kernel_template(kernel_template_client_super_admin: KernelTemplateClient):
    kernel_template = kernel_template_client_super_admin.create_kernel_template(
        kernel_template_id="kt1",
        milli_cpu_limit=200,
        gpu=1,
        memory_bytes_limit="1000",
        max_idle_duration="600s",
    )
    # return the whole resource, not just ID
    yield kernel_template
    kernel_template_client_super_admin.delete_kernel_template(kernel_template_id="kt1")


@pytest.fixture(scope="function")
def delete_all_notebook_kernel_specs_after(notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient):
    yield
    notebook_kernel_spec_client_super_admin.delete_all_notebook_kernel_specs()
