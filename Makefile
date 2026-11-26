.PHONY: install lint test check tf-check run

install:
	pip install -e ".[dev]"

lint:
	ruff check .
	ruff format --check .
	mypy src tests

test:
	pytest

tf-check:
	cd infra/terraform && terraform fmt -check -recursive && terraform init -backend=false -input=false && terraform validate

check: lint test tf-check

run:
	uvicorn cloud_launchpad.app:app --reload
