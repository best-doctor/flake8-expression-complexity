install:
	uv sync

test:
	uv run pytest

coverage:
	uv run pytest --cov=flake8_expression_complexity --cov-report=xml

types:
	uv run mypy .

style:
	uv run flake8 .

readme:
	uv run pre-commit run markdownlint-cli2 --files README.md CHANGELOG.md

requirements:
	uv run pip-audit

precommit:
	uv run pre-commit run --all-files

check:
	make style
	make types
	make test
	make requirements
