#!/bin/bash

# Exit on error
set -e

echo "Running tests for stayup..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pytest with verbosity and show coverage
python -m pytest tests/ -v --cov=stayup --cov-report=term-missing

# Deactivate virtual environment if it was activated
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi
