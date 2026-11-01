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
| `psycopg[binary]` | Psycopg 3 PostgreSQL driver used by SQLAlchemy. The SQLAlchemy URL uses the `postgresql+psycopg://` driver prefix. |

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
postgresql+psycopg://username:password@localhost:5432/database_name
```

If using an asynchronous SQLAlchemy setup, choose an async PostgreSQL driver such as `asyncpg` instead and use the matching SQLAlchemy URL. Do not mix a synchronous driver and URL with async database code.

## Running the Student API with local PostgreSQL

The app loads `DATABASE_URL` from a `.env` file in the project directory. Create that file with your local PostgreSQL connection:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/postgres
```

Replace `YOUR_PASSWORD` with your PostgreSQL password. The default local setup in this workspace uses the `postgres` user, `localhost:5432`, and the default `postgres` database. Ensure the PostgreSQL server is running. The app creates the `students` table on startup. You can also override the `.env` value by setting `DATABASE_URL` in the environment.

Start the API from the project directory:

```powershell
uv run uvicorn student.main:app --reload
```

Add a student by sending this request:

```http
POST /students/
Content-Type: application/json

{"name": "Alex Smith", "age": 18, "grade": "A"}
```

The response contains the new student's database-generated `id`. Retrieve the saved record with `GET /students/{student_id}`.

---

# Pydantic

Pydantic is a Python library for defining data models and validating data. FastAPI uses Pydantic models to validate incoming request data, serialize responses, and describe API schemas in its generated OpenAPI documentation.

## Defining a model

```python
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0)
    email: str
```

`BaseModel` is the base class for a Pydantic model. Type annotations define the expected types, while `Field` can add constraints. When data is parsed into this model, Pydantic checks and converts values when possible; invalid data produces a validation error.

## Common field types

The type annotation tells Pydantic what kind of value a field should contain. These are common Python types used in API schemas:

| Type | Example | Typical use |
|------|---------|-------------|
| `str` | `name: str` | Text such as names, titles, and email addresses. |
| `int` | `age: int` | Whole numbers such as counts or ages. |
| `float` | `score: float` | Decimal measurements or scores. Use `Decimal` for values where exact decimal arithmetic matters, such as money. |
| `bool` | `is_active: bool` | True/false flags. |
| `Decimal` | `price: Decimal` | Exact decimal values; useful for financial amounts. |
| `date` | `birth_date: date` | Calendar dates without a time. |
| `datetime` | `created_at: datetime` | A date and time, such as a creation timestamp. |
| `UUID` | `id: UUID` | UUID identifiers. |
| `list[str]` | `tags: list[str]` | A list of values of one type. Can also be `list[Student]` for nested models. |
| `dict[str, int]` | `scores: dict[str, int]` | Key/value data with declared key and value types. |
| `str \| None` | `nickname: str \| None` | A string that may be `None`. To make it optional in an incoming request, also give it a default, such as `nickname: str \| None = None`. |
| `str \| int` | `code: str \| int` | A value that may have one of several types. Pydantic validates it against the union. |
| `Literal["new", "active"]` | `status: Literal["new", "active"]` | Restricts a value to a fixed set of choices. |
| `Enum` | `role: UserRole` | A named set of choices, especially useful when choices are reused. |
| `Any` | `metadata: Any` | Accepts any value. Use sparingly because it gives up most type validation. |

`Optional[T]` means the same thing as `T | None`; it allows `None`, but does not by itself make a field omittable. A default value makes a field omittable in input. For example, `nickname: str | None` is required but can be `None`, while `nickname: str | None = None` may be omitted.

## What `Field` does

`Field(...)` adds validation rules and schema metadata to one model field. It does not declare the field's type; the type annotation does that. For example, `age: int = Field(ge=0)` means the value must be an integer greater than or equal to zero.

### Common validation parameters

| Parameter | Meaning | Example |
|-----------|---------|---------|
| `gt` | Greater than (exclusive). | `Field(gt=0)` — must be greater than zero. |
| `ge` | Greater than or equal to (inclusive). | `Field(ge=0)` — zero or higher. |
| `lt` | Less than (exclusive). | `Field(lt=150)` — must be less than 150. |
| `le` | Less than or equal to (inclusive). | `Field(le=100)` — at most 100. |
| `multiple_of` | Must be divisible by the given number. | `Field(multiple_of=5)` — a multiple of five. |
| `min_length` | Minimum number of characters or items. | `Field(min_length=1)` — non-empty string or collection. |
| `max_length` | Maximum number of characters or items. | `Field(max_length=100)` — at most 100 characters/items. |
| `pattern` | String must match a regular expression. | `Field(pattern=r"^[A-Z]{2}$")` — exactly two uppercase letters. |
| `strict` | Avoids many automatic type conversions for this field. | `Field(strict=True)` — an input string such as `"4"` is not accepted as an integer. |

Use parameters that apply to the annotated type: numeric limits such as `ge` are for numbers, while `min_length` and `max_length` are for strings or collections. Pydantic reports a validation error when a value fails a constraint.

### Common field metadata and defaults

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `default` | Value used when the field is omitted. | `Field(default=0)` |
| `default_factory` | Creates a fresh default value for each model instance. | `Field(default_factory=list)` |
| `title` | Human-readable field title in generated schema/docs. | `Field(title="Student name")` |
| `description` | Explains the field in generated schema/docs. | `Field(description="Name shown in the class list")` |
| `examples` | Provides example values for API documentation/schema. | `Field(examples=["Ada"])` |
| `alias` | External name used for the field when validating/serializing, depending on configuration. | `Field(alias="studentName")` |
| `deprecated` | Marks a field as deprecated in generated schema/docs. | `Field(deprecated=True)` |

Prefer `default_factory` for mutable defaults such as lists and dictionaries:

```python
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    tags: list[str] = Field(default_factory=list, max_length=10)
```

`default_factory=list` ensures each `StudentCreate` instance gets its own list. `Field` constraints do not replace type annotations: `age: int` says it is an integer, and `ge=0` sets its minimum allowed value.

## Using models in FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    id: int
    name: str


@app.post("/students/", response_model=Student)
def create_student(student: Student) -> Student:
    return Student(id=1, name=student.name)
```

Here, FastAPI validates the JSON request body as a `Student`, and `response_model` documents and filters the response to the declared fields. In a real application, use separate models for input and output when they contain different fields—for example, an input model may omit a database-generated `id`.

## Pydantic and SQLAlchemy

Pydantic schemas and SQLAlchemy models serve different purposes:

- **Pydantic models** validate and serialize data at the API boundary.
- **SQLAlchemy models** represent database tables and manage database persistence.

They can describe related data, but they are not interchangeable. Keep API schemas separate from database models, and explicitly map between them where needed.

For application configuration loaded from environment variables, use `pydantic-settings` and its `BaseSettings` class; it is a separate package from `pydantic`.
