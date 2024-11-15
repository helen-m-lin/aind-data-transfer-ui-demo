"""Core models for using aind-data-transfer-service

Minimal version of SubmitJobRequest from aind-data-transfer-models

### FastUI
Summary fields that cannot be handled:
- upload_jobs list changed to single upload_job

Changes:
- Uses BaseModel instead of BaseSettings
- Uses fields from SubmitJobRequest and parent S3UploadSubmitJobRequest
- Removed:
    - model_config: ConfigDict
    - job_type: Optional[str]
    - @model_validator:
        - propagate_email_settings
- Type changes:
    - upload_job: BasicUploadJobConfigsFastUI instead of List[BasicUploadJobConfigs]
Unchanged:
- user_email
- email_notification_types
    - NOTE: Default value not displayed in form but is set in the submitted data
Added:
- @field_validator('email_notification_types', mode='before')
- _process_form_data(): converts single upload_job to list, also processes upload_job
- process_and_validate_form_data(): validates with aind-data-transfer-models

#### Streamlit Pydantic
- Additionally remove optional fields

"""

import json
from typing import (
    List,
    Optional,
    Set,
)
from aind_data_transfer_models.core import SubmitJobRequest
from aind_data_transfer_models.s3_upload_configs import (
    EmailNotificationType,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
)
from aind_data_transfer_ui_demo.models.basic_upload_job_configs import (
    BasicUploadJobConfigsFastUI,
    BasicUploadJobConfigsSimple,
    BasicUploadJobConfigsStreamlit,
)


class SubmitJobRequestFastUI(BaseModel):
    """Minimal version of SubmitJobRequest from aind-data-transfer-models.
    Combines fields from SubmitJobRequest and parent S3UploadSubmitJobRequest
    """
    
    # S3UploadSubmitJobRequest
    # NOTE: use BaseModel instead of BaseSettings
    # model_config = ConfigDict(use_enum_values=True, extra="allow")
    # NOTE: removed since it should be a constant
    # job_type: Optional[str] = Field(
    #     default="transform_and_upload",
    #     description="Optional tag. Will be made Literal in future versions.",
        
    # )
    # NOTE: NotImplementedError: Array fields are not fully supported, see https://github.com/pydantic/FastUI/pull/52
    # NOTE: converted to use BasicUploadJobConfigsFastUI instead of List[BasicUploadJobConfigs]
    upload_job: BasicUploadJobConfigsFastUI = Field(
        ...,
        description="Upload job to process",
    )

    # S3UploadSubmitJobRequest
    # NOTE: overwritten in SubmitJobRequest
    # job_type: Literal["s3_upload"] = "s3_upload"
    user_email: Optional[EmailStr] = Field(
        default=None,
        description=(
            "Optional email address to receive job status notifications"
        ),
    )
    # NOTE: FastUI not displaying default value
    email_notification_types: Set[EmailNotificationType] = Field(
        default={EmailNotificationType.FAIL},
        description=(
            "Types of job statuses to receive email notifications about"
        ),
    )
    # NOTE: overwritten in SubmitJobRequest
    # upload_jobs: List[S3UploadJobConfigs] = Field(
    #     ...,
    #     description="List of upload jobs to process. Max of 20 at a time.",
    #     min_items=1,
    #     max_items=100,
    # )


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
        # currently only 1 upload_job is supported since FastUI does not support lists
        # so we convert the single job to a list
        if form_data.get("upload_job") is not None and isinstance(
            form_data.get("upload_job"), dict
        ):
            # we also need to process the upload job itself
            processed_upload_job = (
                BasicUploadJobConfigsFastUI._process_form_data(
                    form_data["upload_job"]
                )
            )
            form_data["upload_jobs"] = [processed_upload_job]
            del form_data["upload_job"]
        return form_data

    def process_and_validate_form_data(self) -> str:
        """Tries to create aind-data-transfer-models from the submitted data.
        If the model is not valid, an exception is raised."""
        form_data = json.loads(self.model_dump_json())
        processed_form_data = self._process_form_data(form_data)
        validated_model = SubmitJobRequest(**processed_form_data)
        # return the validated model as a json string
        return validated_model.model_dump_json(indent=3)


class SubmitJobRequestSimple(BaseModel):
    """Minimal version of SubmitJobRequest from aind-data-transfer-models.
    Combines fields from SubmitJobRequest and parent S3UploadSubmitJobRequest
    """
    
    # S3UploadSubmitJobRequest
    # NOTE: use BaseModel instead of BaseSettings
    # model_config = ConfigDict(use_enum_values=True, extra="allow")
    # NOTE: removed since it should be a constant
    # job_type: Optional[str] = Field(
    #     default="transform_and_upload",
    #     description="Optional tag. Will be made Literal in future versions.",
        
    # )
    # NOTE: converted to use List[BasicUploadJobConfigsSimple] instead of List[BasicUploadJobConfigs]
    upload_jobs: List[BasicUploadJobConfigsSimple] = Field(
        ...,
        description="Upload job to process",
        min_items=1,
        max_items=1000,
    )

    # S3UploadSubmitJobRequest
    # NOTE: overwritten in SubmitJobRequest
    # job_type: Literal["s3_upload"] = "s3_upload"
    user_email: Optional[EmailStr] = Field(
        default=None,
        description=(
            "Optional email address to receive job status notifications"
        ),
    )
    email_notification_types: Set[EmailNotificationType] = Field(
        default={EmailNotificationType.FAIL},
        description=(
            "Types of job statuses to receive email notifications about"
        ),
    )

class SubmitJobRequestStreamlit(SubmitJobRequest):
    """Minimal version of SubmitJobRequest from aind-data-transfer-models.
    Combines fields from SubmitJobRequest and parent S3UploadSubmitJobRequest
    """
    job_type: str = Field(
        default="s3_upload",
        description="Job type",
        readOnly=True,
    )
    upload_jobs: List[BasicUploadJobConfigsStreamlit] = Field(
        ...,
        description="Upload job to process",
        min_items=1,
        max_items=1000,
    )
    user_email: EmailStr = Field(
        default=None,
        description=(
            "Optional email address to receive job status notifications"
        ),
    )
    