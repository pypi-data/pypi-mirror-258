# spectral-cli
Python CLI supporting interactions with Challenges on the Spectral Network Platform.

[![PyPI version](https://badge.fury.io/py/spectral-cli.svg)](https://badge.fury.io/py/spectral-cli)

## Overview

**spectral-cli** is a Python command-line interface (CLI) tool. It uses Poetry for package management and provides a set of Makefile commands for common tasks.

## Installation

To install **spectral-cli**, use the following command:

```bash
make install
```

## Usage

### Running Tests

Execute the following command to run the test suite:

```bash
make test
```

### Building the Package

Build the package using the following command:

```bash
make build
```

### Publishing to PyPI

Publish the package to PyPI with the following command:

```bash
make publish
```

### Publishing to TestPyPI

To publish the package to TestPyPI, use the following command:

```bash
make publish-test
```

## Version Management

Bump the version with the following commands:

- Bump patch version: `make bump-patch`
- Bump minor version: `make bump-minor`
- Bump major version: `make bump-major`
