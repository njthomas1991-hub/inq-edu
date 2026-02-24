Param()
Write-Host "Installing/ensuring formatters (this may ask for admin privileges)..."
python -m pip install --upgrade ruff black isort

Write-Host "Running ruff (lint)..."
python -m ruff check --fix .

Write-Host "Running isort..."
python -m isort .

Write-Host "Running black..."
python -m black .

Write-Host "Linting and formatting complete."
