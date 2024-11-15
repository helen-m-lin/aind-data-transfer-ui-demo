# aind-data-transfer-ui-demo

[![License](https://img.shields.io/badge/license-MIT-brightgreen)](LICENSE)
![Code Style](https://img.shields.io/badge/code%20style-black-black)
[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
![Interrogate](https://img.shields.io/badge/interrogate-100.0%25-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=codecov)
![Python](https://img.shields.io/badge/python->=3.10-blue?logo=python)

## Goal
This repo contains demos to evaluate use of FastUI and other pydantic forms generation for aind-data-transfer-service.

- Generate form ui from pydantic models for users to submit job requests to aind-data-transfer-service
- Job config and request models are in `aind-data-transfer-models` library
- Can also consider generating the form from jsonschema
- Evaluate feasibility and limitations of possible options

## Installation
To develop the code, run
```bash
pip install -e .[dev]
```

## Run demos locally

```bash
# FastUI
uvicorn aind_data_transfer_ui_demo.fast_ui.server:app --host 0.0.0.0 --port 8000 --reload
```

### FastUI

Overall limitations:
- Does not support: dict, complex list, PurePosixPath, .ONE_OF, and other complex types
- Need FastAPI infrastructure (currently Starlette)
- UI components relatively straightforward, but can get lengthy
- occasionally buggy/ lack of support
    - e.g. bug with list select multiple requires custom field_validator for all lists


To handle limitations:
1. Convert models from aind-data-transfer-models to minified models.
    - Minified models can have simple type and custom validators.
    - Remove field_validators, model_validators, complex types
    - Convert to BaseModel instead of BaseSettings
    - Take all fields from original model and any parent models
2. Add methods to convert submitted formdata into original aind-data-transfer-models
    - converts flattened fields back to original lists

Fields that cannot be handed from aind-data-transfer-models:
- ModalityConfigs:
    - job_settings: Optional[dict]
    - slurm_settings: Optional[V0036JobProperties]
- BasicUploadJobConfigs:
    - metadata_configs: Optional[GatherMetadataJobSettings]
    - trigger_capsule_configs: Optional[TriggerConfigModel]
    - codeocean_configs: CodeOceanPipelineMonitorConfigs
    - modalities list changed to single modality
- SubmitJobRequest:
    - upload_jobs list changed to single upload_job

Next steps:
- figure out how to attach multiple modalities, upload_jobs
- post form submission to aind-data-transfer-service
- refactor aind-data-transfer-service to FastAPI
- integrate fastui job form + submission
- implement nav bar in fastui
- implement jobs status page in fast ui

### Json Editor

Demo Playground: https://json-editor.github.io/json-editor/

- Can use CDN from `<script src="https://cdn.jsdelivr.net/npm/@json-editor/json-editor@latest/dist/jsoneditor.min.js"></script>`
- All simplified models work in Playground, able to add nested list models.

## Contributing

### Linters and testing

There are several libraries used to run linters, check documentation, and run tests.

- Please test your changes using the **coverage** library, which will run the tests and log a coverage report:

```bash
coverage run -m unittest discover && coverage report
```

- Use **interrogate** to check that modules, methods, etc. have been documented thoroughly:

```bash
interrogate .
```

- Use **flake8** to check that code is up to standards (no unused imports, etc.):
```bash
flake8 .
```

- Use **black** to automatically format the code into PEP standards:
```bash
black .
```

- Use **isort** to automatically sort import statements:
```bash
isort .
```