clean: ## Clean environment
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f *.log

create_virtualenv: ## Create a virtualenv
	python -m venv urlshortner && source urlshortner/bin/activate

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

lint:  ## Lint project
	flake8

run-dev:  ## Run devserver
	python manage.py runserver 0.0.0.0:8002

shell-dev:  ## Run django shell for dev
	python manage.py shell

setup-dev:  ## Install python requirements
	pip install -r requirements.txt

test: clean lint  ## Run tests
	py.test . -vsx
