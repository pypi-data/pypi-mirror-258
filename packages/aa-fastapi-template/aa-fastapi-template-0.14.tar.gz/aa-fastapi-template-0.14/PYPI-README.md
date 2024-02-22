# AA FastAPI Template

A robust and sensible baseline for kick-starting any new FastAPI application. This template provides a comprehensive setup for developing high-performance web applications with FastAPI, including optional, opinionated development and testing dependencies to enhance your development workflow.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

## Installation

    # Using pip:
    pip install aa-fastapi-template

    # tests
    pip install aa-fastapi-template[tests]

    # dev
    pip install aa-fastapi-template[dev]

The base package provides the essential tools for creating FastAPI applications. While `[tests]` only adds testing libraries, the `[dev]` option installs both testing and development tools.

## Package Options

Included within each package are:

| aa-fastapi-template    | aa-fastapi-template[tests]  | aa-fastapi-template[dev]  |
|------------------------|-----------------------------|---------------------------|
| asyncpg                | + aa-fastapi-template       | + aa-fastapi-template[tests] |
| environs               | hypothesis                  | black                     |
| fastapi                | pytest                      | httpx                     |
| mypy                   | pytest-cov                  | ruff                      |
| psycopg2-binary        | pytest-emoji                | toml                      |
| pydantic               | pytest-md                   | types-toml                |
| python-dotenv          | pytest-mock                 |                           |
| sqlalchemy             | pytest-xdist                |                           |
| sqlmodel               |                             |                           |
| uvicorn                |                             |                           |


## Contributing

We welcome contributions to the AA FastAPI Template! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

- Issues: Use the [GitHub Issues page](https://github.com/aaron-imbrock/aa-fastapi-template/issues)
- Pull Requests: Submit pull requests with your changes/fixes.
