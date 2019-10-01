#!/usr/bin/env bash

EXIT_CODE=0

pylint src || EXIT_CODE=1
pylint tests --disable=duplicate-code || EXIT_CODE=1

mypy src || EXIT_CODE=1
mypy tests || EXIT_CODE=1

pycodestyle . || EXIT_CODE=1

python -m flake8 src || EXIT_CODE=1
python -m flake8 tests || EXIT_CODE=1

exit ${EXIT_CODE}
