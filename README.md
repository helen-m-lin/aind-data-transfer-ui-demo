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