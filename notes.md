# Understanding UV Project Structure

`uv` is a modern Python package and project manager developed by Astral. It is designed to replace and simplify tools such as:

- pip
- venv
- pip-tools
- poetry
- pyenv (partially)

It provides fast dependency management, virtual environments, package installation, and project creation.

---

# Creating a New Project

```bash
uv init my-project
```

Typical project structure:

```text
my-project/
│
├── .python-version
├── pyproject.toml
├── README.md
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── main.py
│
└── uv.lock
```

---

# Project Files Explained

## 1. pyproject.toml

The central configuration file for a Python project.

Example:

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My UV project"
dependencies = [
    "requests"
]
```

### Responsibilities

- Project metadata
- Dependencies
- Build configuration
- Tool configuration (ruff, mypy, pytest, etc.)

### Node.js Equivalent

| Python | Node.js |
|----------|----------|
| pyproject.toml | package.json |

---

## 2. uv.lock

Dependency lock file.

Example:

```text
uv.lock
```

### Purpose

Stores:

- Exact package versions
- Transitive dependencies
- Dependency resolution data

Without a lock file:

```text
requests
└── urllib3 (latest version)
```

The installed version may change over time.

With a lock file:

```text
requests==2.32.3
urllib3==2.2.2
```

Every developer installs identical dependency versions.

### Commands

Generate or update:

```bash
uv sync
```

or

```bash
uv add requests
```

### Node.js Equivalent

| Python | Node.js |
|----------|----------|
| uv.lock | package-lock.json |

---

# FastAPI and PostgreSQL Packages

The project dependencies currently include the packages below:

| Package | Why it is needed |
|----------|------------------|
| `fastapi` | Provides the web framework for defining API routes, handling requests, and generating OpenAPI documentation. |
| `pydantic` | Defines and validates data models, such as API request and response schemas. FastAPI uses Pydantic, but listing it directly is useful when the application imports it directly. |
| `sqlalchemy` | Provides database connectivity and SQL/ORM tools for working with PostgreSQL. |
| `psycopg2` | PostgreSQL driver used by SQLAlchemy to communicate with a PostgreSQL server. The SQLAlchemy URL should use the `postgresql+psycopg2://` driver prefix. |

## Additional packages to run and maintain the app

```bash
uv add "uvicorn[standard]" alembic pydantic-settings
```

| Package | Why it is useful |
|----------|------------------|
| `uvicorn[standard]` | ASGI server that runs the FastAPI application. FastAPI defines the app; Uvicorn serves it. |
| `alembic` | Creates and runs database schema migrations as the SQLAlchemy models change. |
| `pydantic-settings` | Loads and validates application settings, such as the database URL, from environment variables or `.env` files. |

For a synchronous SQLAlchemy setup, a PostgreSQL connection URL typically looks like:

```text
postgresql+psycopg2://username:password@localhost:5432/database_name
```

If using an asynchronous SQLAlchemy setup, choose an async PostgreSQL driver such as `asyncpg` instead and use the matching SQLAlchemy URL. Do not mix a synchronous driver and URL with async database code.
