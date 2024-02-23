import http
import os

import pytest

from h2o_notebook.clients.kernel_template.client import KernelTemplateClient
from h2o_notebook.exception import CustomApiException


def test_create_kernel_template_full_params(
    kernel_template_client_super_admin: KernelTemplateClient,
    delete_all_kernel_templates_after,
):
    yaml_spec = open(os.path.join(os.path.dirname(__file__), "pod_template_spec.yaml"), "r").read()

    kt = kernel_template_client_super_admin.create_kernel_template(
        kernel_template_id="my-first-kernel-template",
        milli_cpu_limit=200,
        milli_cpu_request=100,
        gpu_resource="SmokerGPU300Pro",
        gpu=100,
        memory_bytes_limit="500M",
        memory_bytes_request="500M",
        disabled=True,
        max_idle_duration="8h",
        yaml_pod_template_spec=yaml_spec,
        environmental_variables={"key1": "value1", "key2": "value2"},
    )

    assert kt.name == "kernelTemplates/my-first-kernel-template"
    assert kt.kernel_template_id == "my-first-kernel-template"
    assert kt.milli_cpu_limit == 200
    assert kt.milli_cpu_request == 100
    assert kt.gpu == 100
    assert kt.gpu_resource == "SmokerGPU300Pro"
    assert kt.memory_bytes_limit == "500M"
    assert kt.memory_bytes_request == "500M"
    assert kt.max_idle_duration == "8h"
    assert kt.environmental_variables == {"key1": "value1", "key2": "value2"}
    assert kt.yaml_pod_template_spec == yaml_spec
    assert kt.disabled is True
    assert kt.create_time is not None


def test_create_kernel_templates_super_admin(
    delete_all_kernel_templates_after,
    kernel_template_user,
    kernel_template_client_super_admin,
    kernel_template_client_user,
):
    # SuperAdmin can create KernelTemplate.
    kt = kernel_template_client_super_admin.create_kernel_template(
        kernel_template_id="kernel-template-super-admin",
        milli_cpu_limit=200,
        milli_cpu_request=200,
        gpu=1,
        memory_bytes_limit="500M",
        memory_bytes_request="500M",
        max_idle_duration="600s",
    )

    assert kt.name == "kernelTemplates/kernel-template-super-admin"
    assert kt.kernel_template_id == "kernel-template-super-admin"
    assert kt.milli_cpu_limit == 200
    assert kt.gpu == 1
    assert kt.memory_bytes_limit == "500M"
    assert kt.max_idle_duration == "10m"
    assert kt.environmental_variables == {}
    assert kt.yaml_pod_template_spec == ""
    assert kt.gpu_resource == "nvidia.com/gpu"
    assert kt.milli_cpu_request == 200
    assert kt.memory_bytes_request == "500M"
    assert kt.create_time is not None

    # SuperAdmin tries to create already existing KernelTemplate created by him.
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_super_admin.create_kernel_template(
            kernel_template_id="kernel-template-super-admin",
            milli_cpu_limit=200,
            gpu=1,
            memory_bytes_limit="1000",
            max_idle_duration="600s",
        )
    # Already exists
    assert exc.value.status == http.HTTPStatus.CONFLICT

    # SuperAdmin tries to create already existing KernelTemplate created by someone else.
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_super_admin.create_kernel_template(
            kernel_template_id="kernel-template-user",
            milli_cpu_limit=200,
            gpu=1,
            memory_bytes_limit="1000",
            max_idle_duration="600s",
        )
    # Already exists
    # SuperAdmin should know about existence of all KernelTemplates.
    assert exc.value.status == http.HTTPStatus.CONFLICT


def test_create_kernel_templates_user(
    kernel_template_client_user,
    kernel_template_client_super_admin,
    delete_all_kernel_templates_after,
):
    # User can create KernelTemplate.
    kt = kernel_template_client_user.create_kernel_template(
        kernel_template_id="kernel-template-user",
        milli_cpu_limit=200,
        milli_cpu_request=200,
        gpu=1,
        memory_bytes_limit="500M",
        memory_bytes_request="500M",
        max_idle_duration="6s",
    )

    assert kt.name == "kernelTemplates/kernel-template-user"
    assert kt.kernel_template_id == "kernel-template-user"
    assert kt.milli_cpu_limit == 200
    assert kt.gpu == 1
    assert kt.memory_bytes_limit == "500M"
    assert kt.max_idle_duration == "6s"
    assert kt.environmental_variables == {}
    assert kt.yaml_pod_template_spec == ""
    assert kt.gpu_resource == "nvidia.com/gpu"
    assert kt.milli_cpu_request == 200
    assert kt.memory_bytes_request == "500M"
    assert kt.create_time is not None

    # User tries to create already existing KernelTemplate created by him.
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_user.create_kernel_template(
            kernel_template_id="kernel-template-user",
            milli_cpu_limit=200,
            gpu=1,
            memory_bytes_limit="1000",
            max_idle_duration="600s",
        )
    # Already exists (user should know about its existence)
    assert exc.value.status == http.HTTPStatus.CONFLICT

    # User tries to create already existing KernelTemplate created by someone else.
    kernel_template_client_super_admin.create_kernel_template(
        kernel_template_id="kernel-template-super-admin",
        milli_cpu_limit=200,
        gpu=1,
        memory_bytes_limit="1000",
        max_idle_duration="600s",
    )
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_user.create_kernel_template(
            kernel_template_id="kernel-template-super-admin",
            milli_cpu_limit=200,
            gpu=1,
            memory_bytes_limit="1000",
            max_idle_duration="600s",
        )
    # Unauthorized (user shouldn't know about its existence)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
