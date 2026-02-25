#!/usr/bin/env bash
set -euo pipefail
echo "Installing/ensuring formatters (you may want to run this in a virtualenv)..."
python -m pip install --upgrade ruff black isort

echo "Running ruff (lint)..."
python -m ruff check --fix .

echo "Running isort..."
python -m isort .

echo "Running black..."
python -m black .

echo "Linting and formatting complete."
