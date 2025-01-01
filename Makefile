.PHONY: test coverage lint format build

install:
	pip install -e .[lint,dev,test]

test:
	python -m unittest discover -v -s tests

coverage:
# Exclude the tests directory from coverage
	coverage run --source=src -m unittest discover -v -s tests
	coverage report -m

lint:
	ruff check src
	mypy src
	validate-pyproject pyproject.toml
	vulture src


format:
	isort src tests
	black src tests


build:
	python -m build
