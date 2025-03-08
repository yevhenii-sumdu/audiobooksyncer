#!/usr/bin/env bash

echo 'Linting...'
ruff check

echo 'Checking formatting...'
ruff format --check

echo 'Running static type checking...'
mypy .
