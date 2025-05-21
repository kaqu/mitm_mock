#!/bin/bash -e

# Ensure you have activated your virtual environment (e.g., `source .venv/bin/activate`)
# and installed dependencies (e.g., `uv pip install -e .`) before running this script.

echo "Starting mitmMock..."
echo "Proxy will run at localhost:8080 (by default)"
echo "Make sure you have configured your system/device to use this proxy."
echo "Press Ctrl+C to stop."

mitmdump -q -s ./src/mitmmock/interceptor.py
