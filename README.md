# Documentation export example

## Table of Contents
- [Documentation export example](#documentation-export-example)
  - [Table of Contents](#table-of-contents)
  - [Abstract](#abstract)
  - [Install poetry](#install-poetry)
  - [Init project](#init-project)
  - [Add fastapi](#add-fastapi)
  - [Create single-file FastAPI example](#create-single-file-fastapi-example)
  - [Create the Export Script](#create-the-export-script)
  - [Export OpenAPI spec from FastAPI](#export-openapi-spec-from-fastapi)
    - [Adding script to pyproject.toml](#adding-script-to-pyprojecttoml)
    - [Runing script](#runing-script)
    - [Increment version](#increment-version)
  - [Automate in your CI/CD pipeline](#automate-in-your-cicd-pipeline)
    - [Example running script as part of CI/CD pipeline](#example-running-script-as-part-of-cicd-pipeline)



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

Chances are that you’ll use the OpenAPI spec to generate documentation or code. It is important to add metadata to your FastAPI app so that the generated OpenAPI spec is complete.

Firstly, you should tag our endpoints with tags to make sure they are grouped in logical operations. This example does not use routers, but if you do, you need to tag the router instead of the endpoint.

Tags are used by documentation and code generators to group endpoints together. Tags may include spaces and special characters, but we recommend to keep the tags simple. It is common to use either lowercase or Capital Case for tags, like Items in our example.

In addition to tags, we’ll add a description and version metadata to our FastAPI app instance. The description and version will be used in the generated OpenAPI docs on the overview page. You can find the full list of metadata parameters in the FastAPI docs if you need to include additional details in your specification.

## Create the Export Script

By default FastAPI will generate OpenAPI docs under /docs. You can try this out by running the app and navigating to http://localhost:8000/docs.

It is possible to get the OpenAPI JSON directly by navigating to /openapi.json, but we’ll want to extract the document programmatically in order to be able to automate the process. FastAPI does not support exporting the OpenAPI specification directly, but we’ll use a small script to extract it.

## Export OpenAPI spec from FastAPI

### Adding script to pyproject.toml

[tool.poetry.scripts]
build_spec = "app.build_spec:main"

### Runing script

In pyproject.toml

```sh
[tool.poetry]
version = "0.1.0"
```

Run installed script:

```sh
poetry run build_spec
```

This should create an `openapi.json` in `docs/0.1.0` directory.

```sh
INFO: 📂 adding app to sys.path
INFO: 🏭 importing app from main:app
INFO: 📂 creating directory docs/0.1.0
INFO: 🧾 writing OpenAPI spec to docs/0.1.0/openapi.yaml
INFO: 🧾 documentation version='0.1.0' written to docs/0.1.0/openapi.yaml
```

### Increment version

Update basemodel and increment version in pyproject.toml

```sh
[tool.poetry]
version = "0.2.0"
```

Run script again:

```sh
poetry run build_spec
```

This should create an `openapi.json` in `docs/0.2.0` directory.

```sh
INFO: 📂 adding app to sys.path
INFO: 🏭 importing app from main:app
INFO: 📂 creating directory docs/0.2.0
INFO: 🧾 writing OpenAPI spec to docs/0.2.0/openapi.yaml
INFO: 🧾 documentation version='0.2.0' written to docs/0.2.0/openapi.yaml
```

## Automate in your CI/CD pipeline

How you’ll integrate the extraction to your CI/CD depends on what you are trying to accomplish. The three most common ways to approach this are:

* Extract the spec locally and commit it to your repository. Let CI/CD verify the committed spec is up-to-date.
* Extract the spec as part of your CI/CD pipeline, and use the spec as a temporary file to accomplish something (eg. generate a client).
* Extract the spec as part of your CI/CD pipeline, and commit the generated spec to your repository, when merging to main.

The benefit with using a script is that it can also be run locally. Locally committing is often a safe and straight-forward approach, but may occasionally make merging more difficult. If, however, you only need to generate the OpenAPI spec as part of your CI/CD pipeline, you should also consider dedicated runneres.

The benefit of using as part of CI/CD pipeline is that you can pass version argument from outside, and use TAG instead of defined in pyproject.toml file one.

### Example running script as part of CI/CD pipeline

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