PYTHON = uv run python
MAIN_SCRIPT = src/pac-man.py
CONFIG_FILE = config.json

all: install lint run

install:
	uv venv
	uv pip install pygame

run:
	export PYTHONPATH=$PWD
	$(PYTHON) $(MAIN_SCRIPT) $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(CONFIG_FILE)

clean:
	rm -rf */*/__pycache__ .mypy_cache .pytest_cache */__pycache__ __pycache__
	find . -type f -name '*.pyc' -delete

lint:
	uv run flake8 .
	uv run mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	# Optional strict linting
	uv run flake8 .
	uv run mypy --strict .

.PHONY: all install build run debug lint clean