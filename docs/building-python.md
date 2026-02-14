# Building Python Projects

This monorepo uses `uv` for Python package management and workspace handling.

## Project Structure

The Python workspace is defined in `python/pyproject.toml` and includes:

- `python/libs/`: Shared libraries
- `python/apps/`: Applications
- `python/lambdas/`: AWS Lambda functions

## Prerequisites

- `uv` (installed via `curl -LsSf https://astral.sh/uv/install.sh | sh` or your preferred method)
- Python 3.12+

## Managing Dependencies

Dependencies are managed via `uv`.

### Syncing the Environment

To sync the environment with the lockfile:

```bash
cd python
uv sync
```

### Adding Dependencies

To add a dependency to a specific project within the workspace:

```bash
uv add --package <package-name> <dependency>
```

Example:
```bash
uv add --package data-core pandas
```

## Running Commands

Run commands within the project environment using `uv run`.

```bash
uv run --project python pytest
```

## Building Documentation

To build this documentation site:

```bash
uv run --project python mkdocs build
```

To serve it locally:

```bash
uv run --project python mkdocs serve
```
