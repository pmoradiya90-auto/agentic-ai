from typing_extensions import Annotated, TypedDict
from patchwork.common.utils.step_typing import StepTypeConfig


class NexusIqReportInputs(TypedDict, total=False):
    sbom_vdr_file: Annotated[str, StepTypeConfig(is_config=True)]


class NexusIqReportOutputs(TypedDict):
    sbom_vdr_values: dict
