setup:
	pip install -e . --verbose
	pip install -e .[all]

test:
	pytest -s -v tests/test.py
	pytest -s -v tests

coverage:
	coverage-badge -f -o coverage.svg
	pytest --cov=ax_lang tests --cov-report=html

clean:
	rm -rf ax_lang.egg-info build dist

build: clean
	python -m build

pypi_upload:
	python -m twine upload dist/* --skip-existing

checks:
	black ax_lang tests
	isort ax_lang tests
	flake8 ax_lang tests
	mypy ax_lang

release:
	git push --tags
