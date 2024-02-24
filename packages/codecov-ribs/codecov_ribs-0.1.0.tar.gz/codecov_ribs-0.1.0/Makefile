# Codecov CLI version to use
CODECOV_CLI_VERSION := 0.4.1

lint.install:
	pip install -Iv black==22.3.0 isort

lint.check:
	echo "Linting..."
	black --check .
	echo "Sorting..."
	isort --profile black --check .

test_env.install_cli:
	pip install --no-cache-dir codecov-cli==$(CODECOV_CLI_VERSION)
