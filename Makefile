check:
	flake8 .
	mypy .
	python -m pytest --cov=flake8_expression_complexity --cov-report=xml
