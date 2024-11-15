"""Core models for using aind-data-transfer-service

Minimal version of BasicUploadJobConfigs from aind-data-transfer-models

#### FastUI
Summary fields that cannot be handled:
- metadata_configs: Optional[GatherMetadataJobSettings]
- trigger_capsule_configs: Optional[TriggerConfigModel]
- codeocean_configs: CodeOceanPipelineMonitorConfigs
- modalities list changed to single modality

Changes:
- Uses BaseModel instead of BaseSettings
- Creates PlatformEnum from BasicUploadJobConfigs._PLATFORM_MAP
- Removed:
    - model_config: ConfigDict
    - _PLATFORM_MAP: ClassVar
    - _DATETIME_PATTERN1: ClassVar
    - _DATETIME_PATTERN2: ClassVar
    - metadata_configs: Optional[GatherMetadataJobSettings]
    - trigger_capsule_configs: Optional[TriggerConfigModel]
    - codeocean_configs: CodeOceanPipelineMonitorConfigs
        - TODO: consider flattening out elsewhere if needed
    - @computed_field:
        - s3_prefix
    - @field_validator:
        - @field_validator("s3_bucket", mode="before")
        - @field_validator("platform", mode="before")
        - @field_validator("acq_datetime", mode="before")
    - @model_validator:
        - check_computed_field
        - set_trigger_capsule_configs
        - fill_in_metadata_configs
        - set_codeocean_configs
        - map_legacy_codeocean_configs
    - @staticmethod: _get_job_type
- Type changes:
    - platform: PlatformEnum instead of Platform.ONE_OF
    - modality: ModalityConfigsFastUI instead of modalities: List[ModalityConfigs]
    - metadata_dir: str instead of PurePosixPath
Unchanged:
- user_email
- email_notification_types
- project_name
    - TODO: can use /search api to populate options
- input_data_mount
    - TODO: if deprecated, can probably remove from UI
- process_capsule_id
    - TODO: if deprecated, can probably remove from UI
- s3_bucket
- subject_id
- acq_datetime
- metadata_dir_force
- force_cloud_sync
Added:
- @field_validator('email_notification_types', mode='before')
- _process_form_data(): converts single modality to list
- process_and_validate_form_data(): validates with aind-data-transfer-models

#### Streamlit Pydantic
- Additionally remove optional fields

"""

import json
from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional, Set

from aind_data_transfer_models.core import BasicUploadJobConfigs
from aind_data_transfer_models.s3_upload_configs import (
    BucketType,
    EmailNotificationType,
)
from pydantic import BaseModel, EmailStr, Field, field_validator

from aind_data_transfer_ui_demo.models.modality_configs import (
    ModalityConfigsFastUI,
    ModalityConfigsStreamlit,
)

# NOTE: FastUI requires enums for dropdowns, cannot use Platform.ONE_OF
PlatformEnum = Enum("PlatformType", BasicUploadJobConfigs._PLATFORM_MAP)


class BasicUploadJobConfigsFastUI(BaseModel):
    """Minimal version of BasicUploadJobConfigs from aind-data-transfer-models"""

    # NOTE: use BaseModel instead of BaseSettings
    # model_config = ConfigDict(use_enum_values=True, extra="allow")
    # NOTE: created global PlatformEnum instead
    # _PLATFORM_MAP: ClassVar = {
    #     p().abbreviation.upper(): p().abbreviation for p in Platform.ALL
    # }
    # NOTE: Only used in custom validator
    # _DATETIME_PATTERN1: ClassVar = re.compile(
    #     r"^\d{4}-\d{2}-\d{2}[ |T]\d{2}:\d{2}:\d{2}$"
    # )
    # _DATETIME_PATTERN2: ClassVar = re.compile(
    #     r"^\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [APap][Mm]$"
    # )
    user_email: Optional[EmailStr] = Field(
        default=None,
        description=(
            "Optional email address to receive job status notifications"
        ),
    )
    # NOTE: requires field_validator or 422 Unprocessable Entity when select only one
    email_notification_types: Optional[Set[EmailNotificationType]] = Field(
        default=None,
        description=(
            "Types of job statuses to receive email notifications about"
        ),
    )
    # TODO: can eventually use /search api to fill this in
    project_name: str = Field(
        ..., description="Name of project", title="Project Name"
    )
    # TODO: if deprecated, can probably remove from UI
    input_data_mount: Optional[str] = Field(
        default=None,
        description="(deprecated - set codeocean_configs)",
        title="Input Data Mount",
    )
    # TODO: if deprecated, can probably remove from UI
    process_capsule_id: Optional[str] = Field(
        None,
        description="(deprecated - set codeocean_configs)",
        title="Process Capsule ID",
    )
    s3_bucket: Literal[
        BucketType.PRIVATE, BucketType.OPEN, BucketType.SCRATCH
    ] = Field(
        BucketType.PRIVATE,
        description=(
            "Bucket where data will be uploaded. If null, will upload to "
            "default bucket. Uploading to scratch will be deprecated in "
            "future versions."
        ),
        title="S3 Bucket",
    )
    # NOTE: uses PlatformEnum instead of Platform.ONE_OF
    platform: PlatformEnum = Field(
        ..., description="Platform", title="Platform"
    )
    # NOTE: NotImplementedError: Array fields are not fully supported, see https://github.com/pydantic/FastUI/pull/52
    # NOTE: converted to use ModalityConfigsFastUI instead of List[ModalityConfigs]
    modality: ModalityConfigsFastUI = Field(
        ...,
        description="Data collection modality and its directory location",
        title="Modality",
    )
    subject_id: str = Field(..., description="Subject ID", title="Subject ID")
    acq_datetime: datetime = Field(
        ...,
        description="Datetime data was acquired",
        title="Acquisition Datetime",
    )
    # NOTE: had to convert to str from PurePosixPath
    metadata_dir: Optional[str] = Field(
        default=None,
        description="Directory of metadata",
        title="Metadata Directory",
    )
    metadata_dir_force: bool = Field(
        default=False,
        description=(
            "Whether to override metadata from service with metadata in "
            "optional metadata directory"
        ),
        title="Metadata Directory Force",
    )
    force_cloud_sync: bool = Field(
        default=False,
        description=(
            "Force syncing of data folder even if location exists in cloud"
        ),
        title="Force Cloud Sync",
    )
    # NOTE: Cannot render GatherMetadataJobSettings, too nested to flatten out
    # metadata_configs: Optional[GatherMetadataJobSettings] = Field(
    #     default=None,
    #     description="Settings for gather metadata job",
    #     title="Metadata Configs",
    #     validate_default=True,
    # )
    # NOTE: Cannot render TriggerConfigModel, deprecated anyway
    # trigger_capsule_configs: Optional[TriggerConfigModel] = Field(
    #     default=None,
    #     description=(
    #         "(deprecated. Use codeocean_configs) Settings for the codeocean "
    #         "trigger capsule. Validators will set defaults."
    #     ),
    #     title="Trigger Capsule Configs (deprecated. Use codeocean_configs)",
    #     validate_default=True,
    # )
    # NOTE: Cannot render CodeOceanPipelineMonitorConfigs
    # TODO: can consider adding some default values/flattening out
    # codeocean_configs: CodeOceanPipelineMonitorConfigs = Field(
    #     default=CodeOceanPipelineMonitorConfigs(),
    #     description=(
    #         "User can pass custom fields. Otherwise, transfer service will "
    #         "handle setting default values at runtime."
    #     ),
    # )

    # NOTE: this is not an issue anymore?
    # TODO: Fast UI formats datetime as '%Y-%m-%d %H:%M'
    # Misses ss contents: https://github.com/pydantic/FastUI/issues/333
    # @field_validator("acq_datetime", mode="before")
    # def _parse_datetime(cls, datetime_val: Any) -> datetime:
    #     """Parses datetime string to %YYYY-%MM-%DD HH:mm:ss"""
    #     print(datetime_val)
    #     is_str = isinstance(datetime_val, str)
    #     if is_str and re.match(
    #         SimpleJobConfigs._DATETIME_PATTERN1, datetime_val
    #     ):
    #         return datetime.fromisoformat(datetime_val)
    #     elif is_str and re.match(
    #         SimpleJobConfigs._DATETIME_PATTERN2, datetime_val
    #     ):
    #         return datetime.strptime(datetime_val, "%m/%d/%Y %I:%M:%S %p")
    #     elif is_str:
    #         raise ValueError(
    #             "Incorrect datetime format, should be"
    #             " YYYY-MM-DD HH:mm:ss or MM/DD/YYYY I:MM:SS P"
    #         )
    #     else:
    #         return datetime_val

    # FastUI bug where single select is not converted to list
    # NOTE: this needs to be added to any field that is a list
    @field_validator('email_notification_types', mode='before')
    @classmethod
    def correct_select_multiple(cls, v) -> list:
        if isinstance(v, list):
            return v
        else:
            return [v]

    @staticmethod
    def _process_form_data(form_data: dict):
        # currently only 1 modality is supported since FastUI does not support lists
        # so we convert the single modality to a list
        if form_data.get("modality") is not None and isinstance(
            form_data.get("modality"), dict
        ):
            form_data["modalities"] = [form_data["modality"]]
            del form_data["modality"]
        return form_data

    def process_and_validate_form_data(self) -> str:
        """Tries to create aind-data-transfer-models from the submitted data.
        If the model is not valid, an exception is raised."""
        form_data = json.loads(self.model_dump_json())
        processed_form_data = self._process_form_data(form_data)
        validated_model = BasicUploadJobConfigs(**processed_form_data)
        # return the validated model as a json string
        return validated_model.model_dump_json(indent=3)

class BasicUploadJobConfigsSimple(BaseModel):
    """Minimal version of BasicUploadJobConfigs from aind-data-transfer-models"""

    # NOTE: use BaseModel instead of BaseSettings
    # model_config = ConfigDict(use_enum_values=True, extra="allow")
    # NOTE: created global PlatformEnum instead
    # _PLATFORM_MAP: ClassVar = {
    #     p().abbreviation.upper(): p().abbreviation for p in Platform.ALL
    # }
    # NOTE: Only used in custom validator
    # _DATETIME_PATTERN1: ClassVar = re.compile(
    #     r"^\d{4}-\d{2}-\d{2}[ |T]\d{2}:\d{2}:\d{2}$"
    # )
    # _DATETIME_PATTERN2: ClassVar = re.compile(
    #     r"^\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}:\d{2} [APap][Mm]$"
    # )
    user_email: Optional[EmailStr] = Field(
        default=None,
        description=(
            "Optional email address to receive job status notifications"
        ),
    )
    email_notification_types: Optional[Set[EmailNotificationType]] = Field(
        default=None,
        description=(
            "Types of job statuses to receive email notifications about"
        ),
    )
    # TODO: can eventually use /search api to fill this in
    project_name: str = Field(
        ..., description="Name of project", title="Project Name"
    )
    # TODO: if deprecated, can probably remove from UI
    input_data_mount: Optional[str] = Field(
        default=None,
        description="(deprecated - set codeocean_configs)",
        title="Input Data Mount",
    )
    # TODO: if deprecated, can probably remove from UI
    process_capsule_id: Optional[str] = Field(
        None,
        description="(deprecated - set codeocean_configs)",
        title="Process Capsule ID",
    )
    s3_bucket: Literal[
        BucketType.PRIVATE, BucketType.OPEN, BucketType.SCRATCH
    ] = Field(
        BucketType.PRIVATE,
        description=(
            "Bucket where data will be uploaded. If null, will upload to "
            "default bucket. Uploading to scratch will be deprecated in "
            "future versions."
        ),
        title="S3 Bucket",
    )
    # NOTE: uses PlatformEnum instead of Platform.ONE_OF
    platform: PlatformEnum = Field(
        ..., description="Platform", title="Platform"
    )
    # NOTE: converted to use List[ModalityConfigsFastUI] instead of List[ModalityConfigs]
    modalities: List[ModalityConfigsFastUI] = Field(
        ...,
        description="Data collection modalities and their directory location",
        title="Modalities",
        min_items=1,
    )
    subject_id: str = Field(..., description="Subject ID", title="Subject ID")
    acq_datetime: datetime = Field(
        ...,
        description="Datetime data was acquired",
        title="Acquisition Datetime",
    )
    # NOTE: had to convert to str from PurePosixPath
    metadata_dir: Optional[str] = Field(
        default=None,
        description="Directory of metadata",
        title="Metadata Directory",
    )
    metadata_dir_force: bool = Field(
        default=False,
        description=(
            "Whether to override metadata from service with metadata in "
            "optional metadata directory"
        ),
        title="Metadata Directory Force",
    )
    force_cloud_sync: bool = Field(
        default=False,
        description=(
            "Force syncing of data folder even if location exists in cloud"
        ),
        title="Force Cloud Sync",
    )


class BasicUploadJobConfigsStreamlit(BasicUploadJobConfigsSimple):
    """Minimal version of BasicUploadJobConfigs from aind-data-transfer-models"""
    # change any optional fields to required fields
    user_email: EmailStr = Field(
        default=None,
        description=(
            "Optional email address to receive job status notifications"
        ),
    )
    email_notification_types: Set[EmailNotificationType] = Field(
        default=None,
        description=(
            "Types of job statuses to receive email notifications about"
        ),
    )
    input_data_mount: str = Field(
        default=None,
        description="(deprecated - set codeocean_configs)",
        title="Input Data Mount",
    )
    process_capsule_id: str = Field(
        None,
        description="(deprecated - set codeocean_configs)",
        title="Process Capsule ID",
    )
    modalities: List[ModalityConfigsStreamlit] = Field(
        ...,
        description="Data collection modalities and their directory location",
        title="Modalities",
        min_items=1,
    )
    metadata_dir: str = Field(
        default=None,
        description="Directory of metadata",
        title="Metadata Directory",
    )