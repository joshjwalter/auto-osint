.PHONY: install install-dev test test-unit test-integration lint format clean

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest -v

test-unit:
	pytest -v -m unit

test-integration:
	pytest -v -m integration

test-coverage:
	pytest -v --cov=. --cov-report=html --cov-report=term

lint:
	flake8 .
	mypy . --ignore-missing-imports

format:
	black .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .mypy_cache 