# Loci CLI Tool and Client Library
The official Loci CLI tool and Python client library. The CLI tool performs basic Loci Notes tasks from any command line, and the Python library can be used to build other Python clients.

## Docs
https://loci-notes.gitlab.io/clients/cli

## Installation
### Standard
`pip3 install loci-cli`

### Latest
`pip3 install git+https://gitlab.com/loci-notes/loci-cli`

### Development
```bash
pip install poetry
poetry config virtualenvs.in-project true
poetry install --with dev
poetry run loci --help
```

Use VS Code for development and debugging.
