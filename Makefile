.PHONY: help setup install preprocess eda test test-hypothesis pipeline clean clean-all lint format

help:
	@echo "Insurance Risk Analytics - Available Commands"
	@echo "=============================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Initialize project and generate data"
	@echo "  make install        - Install dependencies"
	@echo "  make install-dev    - Install with dev dependencies"
	@echo ""
	@echo "Data Processing:"
	@echo "  make preprocess     - Run data preprocessing"
	@echo ""
	@echo "Analysis:"
	@echo "  make eda            - Run exploratory data analysis"
	@echo "  make test           - Run hypothesis tests"
	@echo "  make test-hypothesis - Run hypothesis testing (alias)"
	@echo ""
	@echo "Pipeline:"
	@echo "  make pipeline       - Run full DVC pipeline"
	@echo "  make pipeline-dry   - Dry run of DVC pipeline"
	@echo ""
	@echo "Development:"
	@echo "  make lint           - Run code linting"
	@echo "  make format         - Format code with black"
	@echo "  make test-unit      - Run unit tests"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Remove generated files"
	@echo "  make clean-all      - Remove all generated files including data"
	@echo "  make clean-cache    - Clean DVC cache"
	@echo ""

setup:
	python scripts/setup.py

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 isort jupyterlab

preprocess:
	python scripts/preprocess.py

eda:
	python scripts/run_eda.py

test: test-hypothesis

test-hypothesis:
	python scripts/run_hypothesis_tests.py

test-unit:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=src --cov-report=html

pipeline:
	dvc repro

pipeline-dry:
	dvc repro --dry

lint:
	flake8 src/ scripts/ tests/ --max-line-length=100

format:
	black src/ scripts/ tests/
	isort src/ scripts/ tests/

clean:
	rm -rf outputs/eda/*.png
	rm -rf .dvc/cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete

clean-all: clean
	rm -rf data/raw/insurance_data.csv
	rm -rf data/processed/
	rm -rf dvc.lock
	rm -rf .dvc/

clean-cache:
	dvc cache remove --all

dvc-init:
	dvc init

dvc-status:
	dvc status

dvc-dag:
	dvc dag

notebook:
	jupyter notebook

.DEFAULT_GOAL := help
