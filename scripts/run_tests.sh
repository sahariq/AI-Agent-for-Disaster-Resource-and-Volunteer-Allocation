#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")/.."

# Run the test suite
pytest tests/ --maxfail=1 --disable-warnings -q