# Contributing

Contributing is great! Here are some guidelines to follow:


# Releases

Releases are done by the maintainers of the project. To make a release, follow these steps:

- bump the version in pyproject.toml
- commit and push the change
- create a PR with a request to add a new tag

# Linting & Formatting

```bash
uvx ruff check
uvx ruff format
```

# Static type checking

```bash
pyright
```

# Testing

```bash
pytest
```

# Docs

To build the documentation, you need to have `sphinx` installed. You can install it with:

```bash
uv sync --group docs
```

Then, you can build the documentation with:

```bash
source .venv/bin/activate
sphinx-build -b html docs/source docs/build
```

```bash
sphinx-apidoc -o docs/source/ skferm
```
