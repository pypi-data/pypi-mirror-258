import http
import os

import pytest

from h2o_notebook.clients.kernel_image.kernel_image import KernelImage
from h2o_notebook.clients.kernel_template.kernel_template import KernelTemplate
from h2o_notebook.clients.notebook_kernel_spec.client import NotebookKernelSpecClient
from h2o_notebook.exception import CustomApiException


def test_delete_notebook_kernel_spec(
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

    notebook_kernel_spec_client_super_admin.delete_notebook_kernel_spec(notebook_kernel_spec_id=k.notebook_kernel_spec_id)

    with pytest.raises(CustomApiException) as exc:
        notebook_kernel_spec_client_super_admin.get_notebook_kernel_spec(
            notebook_kernel_spec_id=k.notebook_kernel_spec_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_delete_notebook_kernel_spec_not_found(
        notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient,
        kernel_image: KernelImage,
        kernel_template: KernelTemplate,
    delete_all_notebook_kernel_specs_after,
):
    with pytest.raises(CustomApiException) as exc:
        notebook_kernel_spec_client_super_admin.delete_notebook_kernel_spec(notebook_kernel_spec_id="not-found")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
