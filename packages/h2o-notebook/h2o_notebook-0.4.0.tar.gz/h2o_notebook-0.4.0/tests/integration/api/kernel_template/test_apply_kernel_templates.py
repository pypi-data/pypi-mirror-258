import http
import os
from typing import List

import pytest

from h2o_notebook.clients.kernel_template.kernel_template import KernelTemplate
from h2o_notebook.clients.kernel_template.kernel_template_config import (
    KernelTemplateConfig,
)
from h2o_notebook.exception import CustomApiException


def test_apply_kernel_templates(
    kernel_template_client_super_admin,
    delete_all_kernel_templates_after,
):
    yaml_spec = open(os.path.join(os.path.dirname(__file__), "pod_template_spec.yaml"), "r").read()

    k1 = KernelTemplateConfig(
        kernel_template_id="my-first-kernel-template",
        milli_cpu_limit=1,
        milli_cpu_request=1,
        gpu=1,
        memory_bytes_limit="20G",
        memory_bytes_request="20G",
        max_idle_duration="1h",
    )
    k2 = KernelTemplateConfig(
        kernel_template_id="my-second-kernel-template",
        milli_cpu_limit=200,
        milli_cpu_request=100,
        gpu_resource="SmokerGPU300Pro",
        gpu=100,
        memory_bytes_limit="1G",
        memory_bytes_request="1G",
        disabled=True,
        max_idle_duration="600s",
        yaml_pod_template_spec=yaml_spec,
        environmental_variables={"key1": "value1", "key2": "value2"},
    )
    k3 = KernelTemplateConfig(
        kernel_template_id="my-third-kernel-template",
        milli_cpu_limit=3,
        milli_cpu_request=3,
        gpu=3,
        memory_bytes_limit="500M",
        memory_bytes_request="500M",
        max_idle_duration="3s",
    )

    configs = [k1, k2, k3]

    kernel_templates = kernel_template_client_super_admin.apply_kernel_templates(configs)

    want_kernel_templates = [
        KernelTemplate(name="kernelTemplates/my-third-kernel-template", milli_cpu_limit=3, gpu=3,
                       memory_bytes_limit="500M", max_idle_duration="3s", milli_cpu_request=3,
                       memory_bytes_request="500M",
                       disabled=False, yaml_pod_template_spec="", gpu_resource="nvidia.com/gpu",
                       environmental_variables={},
                       kernel_template_id="my-third-kernel_template"),
        KernelTemplate(name="kernelTemplates/my-second-kernel-template", milli_cpu_limit=200, gpu=100,
                       memory_bytes_limit="1G", max_idle_duration="10m", milli_cpu_request=100,
                       memory_bytes_request="1G",
                       disabled=True, yaml_pod_template_spec=yaml_spec, gpu_resource="SmokerGPU300Pro",
                       environmental_variables={"key1": "value1", "key2": "value2"},
                       kernel_template_id="my-second-kernel-template"),
        KernelTemplate(name="kernelTemplates/my-first-kernel-template", milli_cpu_limit=1, gpu=1,
                       memory_bytes_limit="20G", max_idle_duration="1h", milli_cpu_request=1,
                       memory_bytes_request="20G",
                       disabled=False, yaml_pod_template_spec="", gpu_resource="nvidia.com/gpu",
                       environmental_variables={},
                       kernel_template_id="my-first-kernel_template"),
    ]

    assert_kernel_templates_equal(want_kernel_templates, kernel_templates)

    kernel_templates = kernel_template_client_super_admin.list_all_kernel_templates()
    assert_kernel_templates_equal(want_kernel_templates, kernel_templates)


def assert_kernel_templates_equal(want_kernel_templates: List[KernelTemplate], kernel_templates: List[KernelTemplate]):
    assert len(want_kernel_templates) == len(kernel_templates)

    for n in range(len(want_kernel_templates)):
        assert kernel_templates[n].create_time is not None

        assert want_kernel_templates[n].name == kernel_templates[n].name
        assert want_kernel_templates[n].kernel_template_id == kernel_templates[n].kernel_template_id
        assert want_kernel_templates[n].milli_cpu_limit == kernel_templates[n].milli_cpu_limit
        assert want_kernel_templates[n].gpu == kernel_templates[n].gpu
        assert want_kernel_templates[n].memory_bytes_limit == kernel_templates[n].memory_bytes_limit
        assert want_kernel_templates[n].max_idle_duration == kernel_templates[n].max_idle_duration
        assert want_kernel_templates[n].environmental_variables == kernel_templates[n].environmental_variables
        assert want_kernel_templates[n].yaml_pod_template_spec == kernel_templates[n].yaml_pod_template_spec
        assert want_kernel_templates[n].disabled == kernel_templates[n].disabled
        assert want_kernel_templates[n].milli_cpu_request == kernel_templates[n].milli_cpu_request
        assert want_kernel_templates[n].memory_bytes_request == kernel_templates[n].memory_bytes_request
        assert want_kernel_templates[n].gpu_resource == kernel_templates[n].gpu_resource


def test_apply_user(
    delete_all_kernel_templates_after,
    kernel_template_super_admin,
    kernel_template_client_user,
    kernel_template_client_super_admin,
):
    # User will apply only his own KernelTemplates, other users' KernelTemplate will be left unchanged.

    # Create user-owned KernelTemplate.
    kernel_template_client_user.create_kernel_template(
        kernel_template_id="kernel-template-user",
        milli_cpu_limit=200,
        milli_cpu_request=200,
        gpu=1,
        memory_bytes_limit="500M",
        memory_bytes_request="500M",
        max_idle_duration="6s",
    )

    all_kernel_templates = kernel_template_client_super_admin.list_all_kernel_templates()
    assert len(all_kernel_templates) == 2
    assert all_kernel_templates[0].name == "kernelTemplates/kernel-template-user"
    assert all_kernel_templates[1].name == "kernelTemplates/kernel-template-super-admin"

    # Apply nothing == User will delete only its own KernelTemplates.
    kernel_template_client_user.apply_kernel_templates(
        kernel_template_configs=[]
    )

    all_kernel_templates = kernel_template_client_super_admin.list_all_kernel_templates()
    assert len(all_kernel_templates) == 1
    assert all_kernel_templates[0].name == "kernelTemplates/kernel-template-super-admin"

    # Apply one KernelTemplate, User will create only its own KernelTemplates.
    kernel_template_client_user.apply_kernel_templates(
        kernel_template_configs=[
            KernelTemplateConfig(
                kernel_template_id="another-user-kernel-template",
                milli_cpu_limit=1,
                milli_cpu_request=1,
                gpu=1,
                memory_bytes_limit="20G",
                memory_bytes_request="20G",
                max_idle_duration="1h",
            )
        ]
    )

    all_kernel_templates = kernel_template_client_super_admin.list_all_kernel_templates()
    assert len(all_kernel_templates) == 2
    assert all_kernel_templates[0].name == "kernelTemplates/another-user-kernel-template"
    assert all_kernel_templates[1].name == "kernelTemplates/kernel-template-super-admin"

    # But when user gets into conflict with another one's KernelTemplate, he should get Unauthorized error.
    # This is not an atomic operation! (something can be already changed, no rollback)
    conflicting_kt = KernelTemplateConfig(
        kernel_template_id="kernel-template-super-admin",
        milli_cpu_limit=1,
        milli_cpu_request=1,
        gpu=1,
        memory_bytes_limit="20G",
        memory_bytes_request="20G",
        max_idle_duration="1h",
    )
    with pytest.raises(CustomApiException) as exc:
        kernel_template_client_user.apply_kernel_templates(
            kernel_template_configs=[conflicting_kt]
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
