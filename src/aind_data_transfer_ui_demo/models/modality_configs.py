"""Core models for using aind-data-transfer-service

Minimal version of ModalityConfigs from aind-data-transfer-models

#### FastUI
Summary fields that cannot be handled:
- job_settings: Optional[dict]
- slurm_settings: Optional[V0036JobProperties]

Changes:
- Uses BaseModel instead of BaseSettings
- Creates ModalityEnum from ModalityConfigs._MODALITY_MAP
- Removed:
    - model_config: ConfigDict
    - _MODALITY_MAP: ClassVar
    - job_settings: Optional[dict]
    - slurm_settings: Optional[V0036JobProperties]
    - @computed_field:
        - output_folder_name
    - @field_validator:
        - @field_validator("modality", mode="before")
        - @field_validator("compress_raw_data", mode="after")
    - @model_validator:
        - check_computed_field
        - check_modality_configs
- Type changes:
    - modality: ModalityEnum instead of Modality.ONE_OF
    - source: str instead of PurePosixPath
    - extra_configs: str instead of PurePosixPath
Unchanged:
- compress_raw_data
Added:
- process_and_validate_form_data(): validates with aind-data-transfer-models

#### Streamlit Pydantic
- Additionally remove optional fields
"""

import json
from enum import Enum
from typing import Optional

from aind_data_transfer_models.core import ModalityConfigs
from pydantic import BaseModel, Field

# NOTE: FastUI requires enums for dropdowns, cannot use Modality.ONE_OF
ModalityEnum = Enum("ModalityType", ModalityConfigs._MODALITY_MAP)

class ModalityConfigsFastUI(BaseModel):
    """Minimal version of ModalityConfigs from aind-data-transfer-models"""

    # NOTE: use BaseModel instead of BaseSettings
    # model_config = ConfigDict(extra="allow")
    # NOTE: created global ModalityEnum instead
    # _MODALITY_MAP: ClassVar = {
    #     m().abbreviation.upper().replace("-", "_"): m().abbreviation
    #     for m in Modality.ALL
    # }
    # NOTE: uses ModalityEnum instead of Modality.ONE_OF
    modality: ModalityEnum = Field(
        ..., description="Data collection modality", title="Modality"
    )
    # NOTE: had to convert to str from PurePosixPath
    source: str = Field(
        ...,
        description="Location of raw data to be uploaded",
        title="Data Source",
    )
    compress_raw_data: Optional[bool] = Field(
        default=None,
        description="Run compression on data",
        title="Compress Raw Data",
        validate_default=True,
    )
    # NOTE: had to convert to str from PurePosixPath
    extra_configs: Optional[str] = Field(
        default=None,
        description=(
            "Location of additional configuration file for compression job."
        ),
        title="Extra Configs",
    )
    # NOTE: cannot render dict
    # job_settings: Optional[dict] = Field(
    #     default=None,
    #     description=(
    #         "Configs to pass into modality compression job. Must be json "
    #         "serializable."
    #     ),
    #     title="Job Settings",
    # )
    # NOTE: cannot render V0036JobProperties
    # slurm_settings: Optional[V0036JobProperties] = Field(
    #     default=None,
    #     description=(
    #         "Custom slurm job properties. `environment` is a required field. "
    #         "Please set it to an empty dictionary. A downstream process will "
    #         "overwrite it."
    #     ),
    #     title="Slurm Settings",
    # )

    def process_and_validate_form_data(self) -> str:
        """Tries to create aind-data-transfer-models from the submitted data.
        If the model is not valid, an exception is raised."""
        form_data = json.loads(self.model_dump_json())
        # nothing needs to be explicitly handled, can pass directly to ModalityConfigs
        validated_model = ModalityConfigs(**form_data)
        # return the validated model as a json string
        return validated_model.model_dump_json(indent=3)

class ModalityConfigsStreamlit(ModalityConfigsFastUI):
    """Minimal version of ModalityConfigs from aind-data-transfer-models"""
    # change any optional fields to required fields
    compress_raw_data: bool = Field(
        default=None,
        description="Run compression on data",
        title="Compress Raw Data",
        validate_default=True,
    )
    extra_configs: str = Field(
        default=None,
        description=(
            "Location of additional configuration file for compression job."
        ),
        title="Extra Configs",
    )
