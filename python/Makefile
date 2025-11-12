setup:
	pip install -e . --verbose
	pip install -e .[dev]

test:
	pytest -s -v tests/test.py

clean:
	rm -rf ax_lang.egg-info build dist

build: clean
	python -m build

pypi_upload:
	python -m twine upload dist/* --skip-existing

