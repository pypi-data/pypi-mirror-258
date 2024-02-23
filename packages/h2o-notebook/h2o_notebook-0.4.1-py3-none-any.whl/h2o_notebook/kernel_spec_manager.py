import os

import grpc
from jupyter_client.kernelspec import KernelSpec
from jupyter_client.kernelspec import KernelSpecManager

from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_image_pb2 import KernelImage
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_image_service_pb2 import (
    GetKernelImageRequest,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_image_service_pb2_grpc import (
    KernelImageServiceStub,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_template_pb2 import KernelTemplate
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_template_service_pb2 import (
    GetKernelTemplateRequest,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.kernel_template_service_pb2_grpc import (
    KernelTemplateServiceStub,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.notebook_kernel_spec_pb2 import (
    NotebookKernelSpec,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.notebook_kernel_spec_service_pb2 import (
    GetNotebookKernelSpecRequest,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.notebook_kernel_spec_service_pb2 import (
    ListNotebookKernelSpecsRequest,
)
from h2o_notebook.gen.ai.h2o.notebook.v1.notebook_kernel_spec_service_pb2_grpc import (
    NotebookKernelSpecServiceStub,
)


class NotebookKernelSpecManager(KernelSpecManager):
    def __init__(self, **kwargs):
        self.log.info("NotebookKernelSpecManager.__init__")
        addr = os.getenv("H2O_NOTEBOOK_SERVER_GRPC_ADDR")
        if not addr:
            raise ValueError("H2O_NOTEBOOK_SERVER_GRPC_ADDR environment variable is not set")

        channel = grpc.insecure_channel(addr)

        # Initialize services
        self.notebook_image_client = KernelImageServiceStub(channel)
        self.notebook_template_client = KernelTemplateServiceStub(channel)
        self.notebook_kernel_spec_client = NotebookKernelSpecServiceStub(channel)

        # Authorize GRPC requests with Kubernetes service account token if not disabled (local testing)
        # TODO: Support projected service account tokens (the token may update, so handle accordingly)
        self.request_metadata = []
        if os.getenv("NOTEBOOK_ENABLE_GRPC_AUTH", 'True').lower() == "false":
            self.log.info("GRPC auth is disabled")
        else:
            path = os.getenv("KUBERNETES_SERVICE_ACCOUNT_TOKEN_FILE", "/var/run/secrets/kubernetes.io/serviceaccount/token")
            self.request_metadata.append(('authorization', 'Bearer ' + read_file(path)))

        # Try calling an endpoint to verify the connection
        self.notebook_kernel_spec_client.ListNotebookKernelSpecs(request=ListNotebookKernelSpecsRequest(), metadata=self.request_metadata)

        super().__init__(**kwargs)

    def get_all_specs(self):
        res = {}

        print("Getting all notebook kernel specs...")

        next_page_token = ""
        while True:
            notebook_kernel_spec_list = self.notebook_kernel_spec_client.ListNotebookKernelSpecs(
                request=ListNotebookKernelSpecsRequest(
                    page_size=0,
                    page_token=next_page_token,
                ),
                metadata=self.request_metadata
            )

            for notebook_kernel_spec in notebook_kernel_spec_list.notebook_kernel_specs:
                res[get_id(notebook_kernel_spec.name)] = {
                    "resource_dir": "",
                    "spec": self.to_kernel_spec(notebook_kernel_spec).to_dict()
                }

            next_page_token = notebook_kernel_spec_list.next_page_token
            if next_page_token == "":
                break
        print(res)
        return res

    def get_kernel_spec(self, notebook_kernel_spec_name) -> KernelSpec:
        return self.to_kernel_spec(
            self.notebook_kernel_spec_client.GetNotebookKernelSpec(
                request=GetNotebookKernelSpecRequest(name=to_name(notebook_kernel_spec_name)),
                metadata=self.request_metadata,
            ).notebook_kernel_spec
        )

    def to_kernel_spec(self, notebook_kernel_spec: NotebookKernelSpec) -> KernelSpec:
        kernel_image: KernelImage = self.notebook_image_client.GetKernelImage(
            request=GetKernelImageRequest(name=notebook_kernel_spec.kernel_image),
            metadata=self.request_metadata).kernel_image

        kernel_template: KernelTemplate = self.notebook_template_client.GetKernelTemplate(
            request=GetKernelTemplateRequest(name=notebook_kernel_spec.kernel_template),
            metadata=self.request_metadata).kernel_template

        return KernelSpec(
            display_name=notebook_kernel_spec.display_name,
            language=NotebookKernelSpecManager.__to_language(kernel_image.type),
            metadata={
                "process_proxy": {
                    "class_name": "enterprise_gateway.services.processproxies.k8s.KubernetesProcessProxy",
                    "config": NotebookKernelSpecManager.__build_config(kernel_image)
                }
            },
            env=NotebookKernelSpecManager.__build_env(is_spark=is_spark_kernel(kernel_image),
                                                      kernel_template=kernel_template),
            argv=NotebookKernelSpecManager.__build_argv(is_spark=is_spark_kernel(kernel_image),
                                                        notebook_kernel_spec_name=notebook_kernel_spec.name),
        )

    @staticmethod
    def __to_language(notebook_kernel_spec_type: int) -> str:
        if notebook_kernel_spec_type in (KernelImage.TYPE_PYTHON, KernelImage.TYPE_SPARK_PYTHON):
            return "python"
        elif notebook_kernel_spec_type in (KernelImage.TYPE_R, KernelImage.TYPE_SPARK_R):
            return "R"
        else:
            raise ValueError("Unknown notebook_kernel_spec type: " + str(notebook_kernel_spec_type))

    @staticmethod
    def __build_config(kernel_image: KernelImage) -> {}:
        cfg = {"image_name": kernel_image.image}
        if is_spark_kernel(kernel_image):
            cfg["executor_image_name"] = kernel_image.image

        return cfg

    @staticmethod
    def __build_env(is_spark: bool, kernel_template: KernelTemplate) -> {}:
        env = {}
        if is_spark:
            env["SPARK_HOME"] = "/opt/spark"
            env["SPARK_OPTS"] = "--master k8s://https://${KUBERNETES_SERVICE_HOST}:${KUBERNETES_SERVICE_PORT} --deploy-mode cluster --name ${KERNEL_USERNAME}-${KERNEL_ID} --conf spark.kubernetes.namespace=${KERNEL_NAMESPACE} --conf spark.kubernetes.driver.label.app=enterprise-gateway --conf spark.kubernetes.driver.label.kernel_id=${KERNEL_ID} --conf spark.kubernetes.driver.label.component=kernel --conf spark.kubernetes.executor.label.app=enterprise-gateway --conf spark.kubernetes.executor.label.kernel_id=${KERNEL_ID} --conf spark.kubernetes.executor.label.component=worker --conf spark.kubernetes.driver.container.image=${KERNEL_IMAGE} --conf spark.kubernetes.executor.container.image=${KERNEL_EXECUTOR_IMAGE} --conf spark.kubernetes.authenticate.driver.serviceAccountName=${KERNEL_SERVICE_ACCOUNT_NAME} --conf spark.kubernetes.submission.waitAppCompletion=false --conf spark.kubernetes.driverEnv.HTTP2_DISABLE=true --conf spark.scheduler.minRegisteredResourcesRatio=1 --conf spark.kubernetes.driver.annotation.cloud.h2o.ai/creator-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.driver.annotation.cloud.h2o.ai/owner-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.driver.label.cloud.h2o.ai/owner=${KERNEL_USER_SUB} --conf spark.kubernetes.driver.label.cloud.h2o.ai/creator=${KERNEL_USER_SUB} --conf spark.kubernetes.driver.label.telemetry.cloud.h2o.ai/include=true --conf spark.kubernetes.executor.annotation.cloud.h2o.ai/creator-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.executor.annotation.cloud.h2o.ai/owner-display-name=${KERNEL_USER_NAME} --conf spark.kubernetes.executor.label.cloud.h2o.ai/owner=${KERNEL_USER_SUB} --conf spark.kubernetes.executor.label.cloud.h2o.ai/creator=${KERNEL_USER_SUB} --conf spark.kubernetes.executor.label.telemetry.cloud.h2o.ai/include=true ${KERNEL_EXTRA_SPARK_OPTS}"
            env["HTTP2_DISABLE"] = "true"
            env["LAUNCH_OPTS"] = ""

        if kernel_template.memory_bytes_limit:
            env["KERNEL_MEMORY_LIMIT"] = str(kernel_template.memory_bytes_limit)
        if kernel_template.memory_bytes_request:
            env["KERNEL_MEMORY"] = str(kernel_template.memory_bytes_request)
        if kernel_template.milli_cpu_limit:
            env["KERNEL_CPUS_LIMIT"] = str(kernel_template.milli_cpu_limit)
        if kernel_template.milli_cpu_request:
            env["KERNEL_CPUS"] = str(kernel_template.milli_cpu_request)
        if kernel_template.gpu:
            env["KERNEL_GPUS_LIMIT"] = str(kernel_template.gpu)
        if kernel_template.gpu:
            env["KERNEL_GPUS"] = str(kernel_template.gpu)

        return env

    # Do not rename original args, they are used by Jupyter later on
    @staticmethod
    def __build_argv(is_spark: bool, notebook_kernel_spec_name: str) -> []:
        server_addr = os.getenv("H2O_NOTEBOOK_SERVER_GRPC_ADDR")
        argv = ["/opt/h2oai/gateway/kernel-pod-builder",
                f"-notebook-server-grpc-addr={server_addr}",
                f"-notebook-kernel-spec-name={get_id(notebook_kernel_spec_name)}",
                "--kernel-id",
                "{kernel_id}",
                "--port-range",
                "{port_range}",
                "--response-address",
                "{response_address}",
                "--public-key",
                "{public_key}"]
        if is_spark:
            argv.append("--spark-context-initialization-mode")
            argv.append("lazy")

        return argv


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


def is_spark_kernel(kernel_image: KernelImage) -> bool:
    if kernel_image.type in (KernelImage.TYPE_SPARK_R, KernelImage.TYPE_SPARK_PYTHON):
        return True

def get_id(name: str) -> str:
    return name.split("/", 1)[1]

def to_name(id: str) -> str:
    return f"notebookKernelSpecs/{id}"