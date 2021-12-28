define test
	poetry run pytest -s tests
endef

define lint
	poetry run flake8 pipeline
endef

setup:
	# Setup poetry
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
	poetry config virtualenvs.path .venv
	poetry config virtualenvs.in-project true
install:
	poetry install
build:
	poetry build
test:
	$(test)
lint-test:
	$(lint)
check:
	$(test)
	$(lint)

