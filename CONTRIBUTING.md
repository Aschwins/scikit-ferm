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

To generate the API documentation, you can use `sphinx-apidoc`. Run the following command to generate the API documentation from the source code:

```bash
sphinx-apidoc -o docs/source/ skferm
```

All of this is automated in the Makefile, so you can also run:

```bash
make dev
```

With `make dev`, you automatically run autodoc and build the documentation in one go. It will then start a local server to preview the documentation. You can access it at `http://localhost:8000`. If you are using WSL, you might need to use the command below to get the correct URL:

```bash
echo "Documentation server: http://$(hostname -I | cut -d' ' -f1):8000"
```

# Github Actions

To run the GitHub Actions locally, you can use the `act` tool. Make sure you have it installed. You can run the actions in offline mode to test them without needing to push to GitHub:

```bash
act --action-offline-mode
act --action-offline-mode -W '.github/workflows/sphinx.yml'  # or only the docs
```
