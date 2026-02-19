#!/usr/bin/env bash

# Script for code checking and formatting
# Usage:
#   ./ci.sh             -> runs ruff check, black, and mypy
#   ./ci.sh check       -> runs ruff check and mypy
#   ./ci.sh format      -> runs only black

set -e  # exit immediately if any command fails

# Default command is 'all' if no argument is provided
CMD=${1:-all}

case "$CMD" in
    all)
        echo "Running full pipeline: ruff, black, mypy"
        ruff check .
        black .
        mypy .
        ;;
    check)
        echo "Running checks only: ruff, mypy"
        ruff check .
        mypy .
        ;;
    format)
        echo "Running formatter only: black"
        black .
        ;;
    build)
        echo "Running checks and building package"
        ./ci.sh check
        rm -rf dist/ build/ terrex.egg-info/
        pip install --upgrade pip build
        python -m build
        echo "Build complete. Check dist/ directory."
        ;;
    pypi)
        echo "Building and uploading to PyPI"
        ./ci.sh build
        pip install --upgrade twine
        twine upload dist/*
        ;;
    *)
        echo "Unknown command: $CMD"
        echo "Usage: $0 [all|check|format|build|pypi]"
        exit 1
        ;;
esac
