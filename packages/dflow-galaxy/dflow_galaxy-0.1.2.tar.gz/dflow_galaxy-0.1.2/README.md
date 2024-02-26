# DFlow Galaxy

[![PyPI version](https://badge.fury.io/py/dflow-galaxy.svg)](https://badge.fury.io/py/dflow-galaxy)
[![Downloads](https://pepy.tech/badge/dflow-galaxy)](https://pepy.tech/project/dflow-galaxy)

Collection of workflows and tools built on top of DFlow and [ai2-kit](https://github.com/chenggroup/ai2-kit).

## Features
* DFlowBuilder: A type friendly wrapper for `DFlow` to build workflows in a more intuitive way.
* Workflows:
  * TESLA (under development): a **T**raining-**E**xploration-**S**creening-**L**abeling workflow designed by **AI4EC** lab. Get inspired by [DPGEN](https://github.com/deepmodeling/dpgen), [DPGEN2](https://github.com/deepmodeling/dpgen2), ported from [ai2-kit](https://github.com/chenggroup/ai2-kit).

## Get Started
`dflow-galaxy` requires Python 3.9+ since it depends on `typing.Annotated`.

To use `dflow-galaxy` as a library, you can install it via pip:

```bash
pip install dflow-galaxy
```

For developers, please use `poetry` to bootstrap the development environment:

```bash
poetry install
poetry shell
```

## Manuals
* [TESLA Workflow](doc/tesla.md)
