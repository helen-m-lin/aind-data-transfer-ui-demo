"""Script to write json schema files for job config models"""

import json
import os

FOLDER = os.path.dirname(os.path.abspath(__file__)) + "/schemas"

# aind-data-transfer-models
from aind_data_transfer_models.core import (
    BasicUploadJobConfigs,
    SubmitJobRequest,
)
# Fast UI mini models
from aind_data_transfer_ui_demo.models.modality_configs import ModalityConfigsFastUI
from aind_data_transfer_ui_demo.models.basic_upload_job_configs import BasicUploadJobConfigsFastUI
from aind_data_transfer_ui_demo.models.submit_job_request import SubmitJobRequestFastUI
# Simplified mini models (without FastUI flatten lists)
from aind_data_transfer_ui_demo.models.basic_upload_job_configs import BasicUploadJobConfigsSimple
from aind_data_transfer_ui_demo.models.submit_job_request import SubmitJobRequestSimple

models_to_write = [
    SubmitJobRequest,
    BasicUploadJobConfigs,
    ModalityConfigsFastUI,
    BasicUploadJobConfigsFastUI,
    SubmitJobRequestFastUI,
    BasicUploadJobConfigsSimple,
    SubmitJobRequestSimple,
]

for model in models_to_write:
    filename = model.__name__ + ".json"
    with open(FOLDER + "/" + filename, "w") as f:
        json.dump(model.model_json_schema(by_alias=True), f, indent=3)
    print(f"Created {filename}")
