# Documentation export example

## Table of Contents
- [Documentation export example](#documentation-export-example)
  - [Table of Contents](#table-of-contents)
  - [Abstract](#abstract)
  - [Install poetry](#install-poetry)
  - [Init project](#init-project)
  - [Add fastapi](#add-fastapi)
  - [Create single-file FastAPI example](#create-single-file-fastapi-example)
  - [Creating the export script](#creating-the-export-script)
  - [Export OpenAPI spec from FastAPI](#export-openapi-spec-from-fastapi)
    - [Add script to pyproject.toml](#add-script-to-pyprojecttoml)
    - [Running script](#running-script)
    - [Increment version](#increment-version)
  - [Automate in your CI/CD pipeline](#automate-in-your-cicd-pipeline)
    - [Example of running script as part of CI/CD pipeline](#example-of-running-script-as-part-of-cicd-pipeline)



## Abstract

FastAPI is a modern Python web framework for building APIs. FastAPI is a great choice for building simple APIs, and it comes with built-in support for generating OpenAPI documentation.

We will generate and save versioning OpenAPI specification from a FastAPI project.

## Install poetry

```sh
pip install poetry
```

## Init project

```sh
poetry init
```

## Add fastapi

```sh
poetry add fastapi[all]
```

## Create single-file FastAPI example

Chances are you'll be using the OpenAPI spec to generate documentation or code. It is important to add metadata to your FastAPI application so that the generated OpenAPI spec is complete.

Firstly, you should tag our endpoints to ensure that they are grouped into logical operations. This example does not use routers, but if you do, you will need to tag the router instead of the endpoint.

Tags are used by documentation and code generators to group endpoints. Tags can contain spaces and special characters, but we recommend that you keep them simple. It is common to use either lower or upper case for tags, such as Items in our example.

In addition to tags, we'll add a description and version metadata to our FastAPI app instance. The description and version will be used in the generated OpenAPI documentation on the overview page. The full list of metadata parameters can be found in the FastAPI docs if you need to include additional details in your specification.

## Creating the export script

By default FastAPI creates OpenAPI docs under /docs. You can test this by running the application and navigating to `http://localhost:8000/docs`.

It is possible to get the OpenAPI JSON directly by navigating to /openapi.json, but we'll want to extract the document programmatically to automate the process. FastAPI doesn't support exporting the OpenAPI specification directly, but we'll use a little script to extract it.

## Export OpenAPI spec from FastAPI

### Add script to pyproject.toml

```sh
[tool.poetry.scripts]
build_spec = "app.build_spec:main"
```

### Running script

In pyproject.toml

```sh
[tool.poetry]
version = "0.1.0"
```

Run the installed script:

```sh
poetry run build_spec
```

This should create an `openapi.json` in the `docs/0.1.0` directory.

```sh
INFO: 📂 adding app to sys.path
INFO: 🏭 importing app from main:app
INFO: 📂 creating directory docs/0.1.0
INFO: 🧾 writing OpenAPI spec to docs/0.1.0/openapi.yaml
INFO: 🧾 documentation version='0.1.0' written to docs/0.1.0/openapi.yaml
```

### Increment version

Update `BaseModel` and increment `version` in `pyproject.toml`

```sh
[tool.poetry]
version = "0.2.0"
```

Run the script again:

```sh
poetry run build_spec
```

This should create an `openapi.json` in the `docs/0.2.0` directory.

```sh
INFO: 📂 adding app to sys.path
INFO: 🏭 importing app from main:app
INFO: 📂 creating directory docs/0.2.0
INFO: 🧾 writing OpenAPI spec to docs/0.2.0/openapi.yaml
INFO: 🧾 documentation version='0.2.0' written to docs/0.2.0/openapi.yaml
```

## Automate in your CI/CD pipeline

How you integrate extraction into your CI/CD depends on what you're trying to achieve. The three most common approaches are:

* Extract the spec locally and commit it to your repository. Have the CI/CD check that the committed spec is up to date.
* Extract the spec as part of your CI/CD pipeline, and use the spec as a temporary file to accomplish something (e.g. build a client).
* Extract the spec as part of your CI/CD pipeline, and commit the generated spec to your repository when you merge into main.

The advantage of using a script is that it can also be run locally. Committing locally is often a safe and straightforward approach, but can occasionally make merging more difficult. However, if you only need to generate the OpenAPI spec as part of your CI/CD pipeline, you should also consider dedicated runners.

The advantage of using this as part of the CI/CD pipeline is that you can pass the `version` argument externally, and use `TAG` instead of one defined in the `pyproject.toml`

### Example of running script as part of CI/CD pipeline

```sh
export CICD_TAG=2023-01-release
poetry run build_spec --version $CICD_TAG
```

```sh
INFO: 📂 adding app to sys.path
INFO: 🏭 importing app from main:app
INFO: 📂 creating directory docs/2023-01-release
INFO: 🧾 writing OpenAPI spec to docs/2023-01-release/openapi.yaml
INFO: 🧾 documentation version='2023-01-release' written to docs/2023-01-release/openapi.yaml
```
