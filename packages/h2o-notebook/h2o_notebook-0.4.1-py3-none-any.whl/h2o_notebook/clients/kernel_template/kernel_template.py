import pprint
from typing import Dict
from typing import List
from typing import Optional

from h2o_notebook.clients.convert.duration_convertor import duration_to_seconds
from h2o_notebook.clients.convert.duration_convertor import seconds_to_duration
from h2o_notebook.clients.convert.quantity_convertor import number_str_to_quantity
from h2o_notebook.clients.convert.quantity_convertor import quantity_to_number_str
from h2o_notebook.gen.model.v1_kernel_template import V1KernelTemplate


class KernelTemplate:
    def __init__(self,
                 name: str,
                 kernel_template_id: str,
                 memory_bytes_limit: str,
                 gpu: int,
                 max_idle_duration: str,
                 environmental_variables: Dict[str, str] = None,
                 yaml_pod_template_spec: str = "",
                 gpu_resource: str = "",
                 milli_cpu_request: int = 0,
                 milli_cpu_limit: int = 0,
                 memory_bytes_request: str = "0",
                 disabled: bool = False,
                 create_time: Optional[str] = None,
                 update_time: Optional[str] = None,
                 ):
        self.name = name
        self.kernel_template_id = kernel_template_id
        self.milli_cpu_limit = milli_cpu_limit
        self.gpu = gpu
        self.memory_bytes_limit = memory_bytes_limit
        self.max_idle_duration = max_idle_duration
        self.environmental_variables = environmental_variables
        self.yaml_pod_template_spec = yaml_pod_template_spec
        self.gpu_resource = gpu_resource
        self.milli_cpu_request = milli_cpu_request
        self.memory_bytes_request = memory_bytes_request
        self.disabled = disabled
        self.create_time = create_time
        self.update_time = update_time

        self.kernel_template_id = ""
        if name:
            self.kernel_template_id = self.name.split("/")[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def to_api_object(self) -> V1KernelTemplate:
        return V1KernelTemplate(
            name=self.name,
            kernel_template_id=self.kernel_template_id,
            gpu=self.gpu,
            memory_bytes_limit=quantity_to_number_str(self.memory_bytes_limit),
            max_idle_duration=duration_to_seconds(self.max_idle_duration),
            environmental_variables=self.environmental_variables,
            yaml_pod_template_spec=self.yaml_pod_template_spec,
            gpu_resource=self.gpu_resource,
            milli_cpu_request=self.milli_cpu_request,
            millicpu_limit=self.milli_cpu_limit,
            memory_bytes_request=quantity_to_number_str(self.memory_bytes_request),
            disabled=self.disabled,
        )


def from_api_object(api_object: V1KernelTemplate) -> KernelTemplate:
    return KernelTemplate(
        name=api_object.name,
        kernel_template_id=api_object.kernel_template_id,
        milli_cpu_limit=api_object.milli_cpu_limit,
        gpu=api_object.gpu,
        memory_bytes_limit=number_str_to_quantity(api_object.memory_bytes_limit),
        max_idle_duration=seconds_to_duration(api_object.max_idle_duration),
        environmental_variables=api_object.environmental_variables,
        yaml_pod_template_spec=api_object.yaml_pod_template_spec,
        gpu_resource=api_object.gpu_resource,
        milli_cpu_request=api_object.milli_cpu_request,
        memory_bytes_request=number_str_to_quantity(api_object.memory_bytes_request),
        disabled=api_object.disabled,
        create_time=api_object.create_time,
        update_time=api_object.update_time,
    )
