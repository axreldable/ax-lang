# Contributing to the repo

## Development Setup

### 1. Clone

```bash
# Clone the repository
git clone https://github.com/axreldable/ax-lang.git
cd ax-lang
```

### 2. Create python env and install

```bash
python -m venv .venv
cd python
pip install -e ".[all]"
```

## Running Checks

### 1. Unit tests

```bash
pytest -v tests
```

### 2. Tests with coverage

```bash
pytest --cov=ax_lang tests --cov-report=html
```

### 3. All checks before commit

```bash
pytest -v tests
pre-commit run --all-files
axlang expr "((lambda (x) (* x x)) 2)"
axlang file ../examples/test.ax
```

Find coverage in `python/coverage_reports/index.html`.

## Debugging

### 1. Run a unit tests with debug logging

```bash
pytest -v -s tests/functions/test_user_define_functions.py::test_simple_udf --log-cli-level=DEBUG
```

## Release Process

### 1. Bump version

Increase version in the `python/pyproject.toml` file, e.g. `0.10.0` -> `0.11.0`

### 2. Creating release

```bash
# Tag release (triggers automated pipeline)
git tag v1.2.3
git push origin v1.2.3
git push --tags
```

## Documentation development

### 1. Install dependencies

```bash
cd python && pip install -e .[doc]
```

### 2. Generate docs

```bash
cd python && mkdocs build # generates static HTML files in the site/ directory
cd python && mkdocs serve # starts a local development server (http://127.0.0.1:8000) where you can preview the docs
```

### 3. Deploy docs

Docs are deployed automatically via CI on the release.
