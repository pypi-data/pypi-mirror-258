import http

import pytest

from h2o_notebook.exception import CustomApiException


def test_get_kernel_template_super_admin(
    kernel_template_user,
    kernel_template_super_admin,
    kernel_template_client_super_admin,
):
    # SuperAdmin can get its own KernelTemplate
    kt = kernel_template_client_super_admin.get_kernel_template(kernel_template_id="kernel-template-super-admin")

    assert kt.name == "kernelTemplates/kernel-template-super-admin"
    assert kt.kernel_template_id == "kernel-template-super-admin"
    assert kt.milli_cpu_limit == 200
    assert kt.gpu == 1
    assert kt.memory_bytes_limit == "1M"
    assert kt.max_idle_duration == "1h"
    assert kt.environmental_variables == {}
    assert kt.yaml_pod_template_spec == ""
    assert kt.gpu_resource == "nvidia.com/gpu"
    assert kt.milli_cpu_request == 200
    assert kt.memory_bytes_request == "1M"
    assert kt.create_time is not None

    # SuperAdmin can get someone else's KernelTemplate
    kt = kernel_template_client_super_admin.get_kernel_template(kernel_template_id="kernel-template-user")

    assert kt.name == "kernelTemplates/kernel-template-user"
    assert kt.kernel_template_id == "kernel-template-user"
    assert kt.milli_cpu_limit == 200
    assert kt.gpu == 1
    assert kt.memory_bytes_limit == "1M"
    assert kt.max_idle_duration == "1h"
    assert kt.environmental_variables == {}
    assert kt.yaml_pod_template_spec == ""
    assert kt.gpu_resource == "nvidia.com/gpu"
    assert kt.milli_cpu_request == 200
    assert kt.memory_bytes_request == "1M"
    assert kt.create_time is not None

    # SuperAdmin tries to get non-existing KernelTemplate
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_super_admin.get_kernel_template(
            kernel_template_id="kernel-template-non-existing",
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_get_kernel_template_user(
    kernel_template_user,
    kernel_template_super_admin,
    kernel_template_client_user,
):
    # User can get its own KernelTemplate
    kt = kernel_template_client_user.get_kernel_template(kernel_template_id="kernel-template-user")

    assert kt.name == "kernelTemplates/kernel-template-user"
    assert kt.kernel_template_id == "kernel-template-user"
    assert kt.milli_cpu_limit == 200
    assert kt.gpu == 1
    assert kt.memory_bytes_limit == "1M"
    assert kt.max_idle_duration == "1h"
    assert kt.environmental_variables == {}
    assert kt.yaml_pod_template_spec == ""
    assert kt.gpu_resource == "nvidia.com/gpu"
    assert kt.milli_cpu_request == 200
    assert kt.memory_bytes_request == "1M"
    assert kt.create_time is not None

    # User cannot Get someone else's KernelTemplate
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_user.get_kernel_template(
            kernel_template_id="kernel-template-super-admin",
        )
    # User should get unauthorized.
    assert exc.value.status == http.HTTPStatus.FORBIDDEN

    # User tries to get non-existing KernelTemplate
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_user.get_kernel_template(
            kernel_template_id="kernel-template-non-existing",
        )
    # User should get unauthorized
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
