# Script to insert kernelspecs into the database [as is 1.12.2023]
import os

import h2o_authn

import h2o_notebook
from h2o_notebook.clients.kernel_image.kernel_image_config import KernelImageConfig
from h2o_notebook.clients.kernel_image.type import KernelImageType
from h2o_notebook.clients.kernel_template.kernel_template_config import (
    KernelTemplateConfig,
)
from h2o_notebook.clients.notebook_kernel_spec.notebook_kernel_spec_config import (
    NotebookKernelSpecConfig,
)

super_admin_token = os.getenv("SUPER_ADMIN_TOKEN")
if not super_admin_token:
    raise ValueError("SUPER_ADMIN_TOKEN environment variable is not set")

notebook_server_url = os.getenv("NOTEBOOK_SERVER_URL")
if not notebook_server_url:
    raise ValueError("NOTEBOOK_SERVER_URL environment variable is not set")

issuer_url = os.getenv("ISSUER_URL")
if not issuer_url:
    raise ValueError("ISSUER_URL environment variable is not set")

client_id = os.getenv("CLIENT_ID")
if not client_id:
    raise ValueError("CLIENT_ID environment variable is not set")

tp = h2o_authn.TokenProvider(refresh_token=super_admin_token, issuer_url=issuer_url, client_id=client_id)

clients = h2o_notebook.login_custom(
    endpoint=notebook_server_url,
    refresh_token=super_admin_token,
    issuer_url=issuer_url,
    client_id=client_id,
)

python_image = KernelImageConfig(
    kernel_image_id="python",
    kernel_image_type=KernelImageType.TYPE_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-py:0.4.0",
    display_name="Python",
    disabled=False,
)

r_image = KernelImageConfig(
    kernel_image_id="r",
    kernel_image_type=KernelImageType.TYPE_R,
    image="gcr.io/vorvan/h2oai/h2o-kernel-r:0.4.0",
    display_name="R",
    disabled=False,
)

python_spark_image = KernelImageConfig(
    kernel_image_id="python-spark",
    kernel_image_type=KernelImageType.TYPE_SPARK_PYTHON,
    image="gcr.io/vorvan/h2oai/h2o-kernel-pyspark:0.4.0",
    display_name="Spark - Python",
    disabled=False,
)

r_spark_image = KernelImageConfig(
    kernel_image_id="r-spark",
    kernel_image_type=KernelImageType.TYPE_SPARK_R,
    image="gcr.io/vorvan/h2oai/h2o-kernel-sparkr:0.4.0",
    display_name="Spark - R",
    disabled=False,
)

template = KernelTemplateConfig(
    kernel_template_id="local",
    gpu=0,
    memory_bytes_limit="1Gi",
    max_idle_duration="1h",
)

template_gpu = KernelTemplateConfig(
    kernel_template_id="local-gpu",
    gpu=1,
    memory_bytes_limit="1Gi",
    max_idle_duration="1h",
    yaml_pod_template_spec='''
spec:
  containers:
    - name: kernel
  tolerations:
    - effect: NoSchedule
      key: dedicated
      operator: Equal
      value: steam
'''
)

python = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="python-default",
    display_name="Python",
    kernel_image_id=python_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

python_gpu = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="python-gpu",
    display_name="Python [GPU]",
    kernel_image_id=python_image.kernel_image_id,
    kernel_template_id=template_gpu.kernel_template_id,
)

python_l = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="python-l",
    display_name="Python [L]",
    kernel_image_id=python_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

python_xl = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="python-xl",
    display_name="Python [XL]",
    kernel_image_id=python_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

r = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="r",
    display_name="R",
    kernel_image_id=r_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

r_l = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="r-l",
    display_name="R [L]",
    kernel_image_id=r_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

python_spark = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="python-spark",
    display_name="Spark - Python",
    kernel_image_id=python_spark_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

r_spark = NotebookKernelSpecConfig(
    notebook_kernel_spec_id="r-spark",
    display_name="Spark - R",
    kernel_image_id=r_spark_image.kernel_image_id,
    kernel_template_id=template.kernel_template_id,
)

print("Creating default KernelImages, KernelTemplates and NotebookKernelSpecs...")
clients.notebook_kernel_spec_client.apply_kernel_images_templates_notebook_specs(
    kernel_image_configs=[
        python_image,
        r_image,
        python_spark_image,
        r_spark_image,
    ],
    kernel_template_configs=[template, template_gpu],
    notebook_kernel_spec_configs=[
        python,
        python_l,
        python_xl,
        python_gpu,
        r,
        r_l,
        python_spark,
        r_spark,
    ]
)
print("Default NotebookKernelSpecs created.")
