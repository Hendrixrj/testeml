.PHONY: help clean setup run pep8 tests tests_ci check-env-vars

CWD="`pwd`"
PROJECT_NAME = vault
PROJECT_HOME = $(CWD)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean: ## Clear *.pyc files, etc
	@echo "Cleaning up *.pyc files"
	@find . -name "*.pyc" -delete
	@find . -name "*.~" -delete

setup: ## Install project dependencies and some git hooks
	@echo "Installing dependencies..."
	@pip install -r $(PROJECT_HOME)/requirements.txt

pep8: ## Check source-code for PEP8 compliance
	@echo "Checking source-code PEP8 compliance"
	@-pep8 $(PROJECT_HOME) --ignore=E501,E126,E127,E128

tests: clean pep8 ## Run pep8 and all tests with coverage
	@echo "Running pep8 and all tests with coverage"
	@py.test --cov-config .coveragerc --cov $(PROJECT_HOME) --cov-report term-missing

run: check-env-vars clean ## Run a Vault development web server
	@python $(PROJECT_HOME)/manage.py runserver 0.0.0.0:8000

tests_ci: clean pep8 ## Run pep8 and all tests
	@py.test