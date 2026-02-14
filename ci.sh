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
    *)
        echo "Unknown command: $CMD"
        echo "Usage: $0 [all|check|format]"
        exit 1
        ;;
esac
