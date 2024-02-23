import http

import pytest

from h2o_notebook.clients.kernel_image.kernel_image import KernelImage
from h2o_notebook.clients.kernel_template.kernel_template import KernelTemplate
from h2o_notebook.clients.notebook_kernel_spec.client import NotebookKernelSpecClient
from h2o_notebook.exception import CustomApiException


def test_create_notebook_kernel_spec_default_values(
    notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient,
    kernel_image: KernelImage,
    kernel_template: KernelTemplate,
    delete_all_notebook_kernel_specs_after,
):
    k = notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="my-first-notebook-spec",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )

    assert k.name == "notebookKernelSpecs/my-first-notebook-spec"
    assert k.kernel_image == kernel_image.name
    assert k.kernel_template == kernel_template.name
    assert k.display_name == ""
    assert k.disabled is False


def test_create_notebook_kernel_spec_full_params(
    notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient,
    kernel_image: KernelImage,
    kernel_template: KernelTemplate,
    delete_all_notebook_kernel_specs_after,
):
    k = notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="my-first-notebook-spec",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
        display_name="My First Notebook Spec",
        disabled=True,
    )

    assert k.name == "notebookKernelSpecs/my-first-notebook-spec"
    assert k.kernel_image == kernel_image.name
    assert k.kernel_template == kernel_template.name
    assert k.display_name == "My First Notebook Spec"
    assert k.disabled is True


def test_create_notebook_kernel_spec_already_exists(
    notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient,
    kernel_image: KernelImage,
    kernel_template: KernelTemplate,
    delete_all_notebook_kernel_specs_after,
):
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="my-first-notebook-spec",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )

    with pytest.raises(CustomApiException) as exc:
        # Try to create NotebookKernelSpec with the same ID.
        notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
            notebook_kernel_spec_id="my-first-notebook-spec",
            kernel_image_id=kernel_image.kernel_image_id,
            kernel_template_id=kernel_template.kernel_template_id,
        )

    # grpc AlreadyExists == http Conflict 409
    assert exc.value.status == http.HTTPStatus.CONFLICT


def test_create_notebook_kernel_spec_user(
    notebook_kernel_spec_client_user,
    delete_all_notebook_kernel_specs_after,
):
    with pytest.raises(CustomApiException) as exc:
        notebook_kernel_spec_client_user.create_notebook_kernel_spec(
            notebook_kernel_spec_id="whatever",
            kernel_image_id="whatever",
            kernel_template_id="whatever",
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
