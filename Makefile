define test
	poetry run pytest -s tests
endef

define lint
	poetry run flake8 pipeline
endef

define run_circle_ci
	circleci local execute
endef

setup:
	# Setup poetry
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
	poetry config virtualenvs.path .venv
	poetry config virtualenvs.in-project true

	# Install circleci
	curl -fLSs https://raw.githubusercontent.com/CircleCI-Public/circleci-cli/master/install.sh | sudo bash
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
	$(run_circle_ci)

