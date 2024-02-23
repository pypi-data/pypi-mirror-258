import http

import pytest

from h2o_notebook.clients.kernel_image.kernel_image import KernelImage
from h2o_notebook.clients.kernel_template.kernel_template import KernelTemplate
from h2o_notebook.clients.notebook_kernel_spec.client import NotebookKernelSpecClient
from h2o_notebook.exception import CustomApiException


@pytest.mark.parametrize(
    ["page_size", "page_token"],
    [
        (-20, ""),
        (0, "non-existing-token"),
    ],
)
def test_list_validation(
        notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient, page_size, page_token
):
    with pytest.raises(CustomApiException) as exc:
        notebook_kernel_spec_client_super_admin.list_notebook_kernel_specs(
            page_size=page_size,
            page_token=page_token,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_list(
        notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient,
        kernel_image: KernelImage,
        kernel_template: KernelTemplate,
    delete_all_notebook_kernel_specs_after,
):
    # Test no profiles found.
    page = notebook_kernel_spec_client_super_admin.list_notebook_kernel_specs()
    assert len(page.notebook_kernel_specs) == 0
    assert page.next_page_token == ""

    # Arrange
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="spec1",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="spec2",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="spec3",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )

    # Test getting first page.
    page = notebook_kernel_spec_client_super_admin.list_notebook_kernel_specs(page_size=1)
    assert len(page.notebook_kernel_specs) == 1
    assert page.next_page_token != ""

    # Test getting second page.
    page = notebook_kernel_spec_client_super_admin.list_notebook_kernel_specs(
        page_size=1, page_token=page.next_page_token
    )
    assert len(page.notebook_kernel_specs) == 1
    assert page.next_page_token != ""

    # Test getting last page.
    page = notebook_kernel_spec_client_super_admin.list_notebook_kernel_specs(
        page_size=1, page_token=page.next_page_token
    )
    assert len(page.notebook_kernel_specs) == 1
    assert page.next_page_token == ""

    # Test exceeding max page size.
    page = notebook_kernel_spec_client_super_admin.list_notebook_kernel_specs(page_size=1001)
    assert len(page.notebook_kernel_specs) == 3
    assert page.next_page_token == ""


def test_list_all(
        notebook_kernel_spec_client_super_admin: NotebookKernelSpecClient,
        kernel_image: KernelImage,
        kernel_template: KernelTemplate,
    delete_all_notebook_kernel_specs_after,
):
    # Arrange
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="spec1",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="spec2",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )
    notebook_kernel_spec_client_super_admin.create_notebook_kernel_spec(
        notebook_kernel_spec_id="spec3",
        kernel_image_id=kernel_image.kernel_image_id,
        kernel_template_id=kernel_template.kernel_template_id,
    )

    # Test basic list_all.
    kernelspecs = notebook_kernel_spec_client_super_admin.list_all_notebook_kernel_specs()
    assert len(kernelspecs) == 3
