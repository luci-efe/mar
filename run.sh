#!/bin/bash
# Simple run script for the interactive video player

# Change to script directory
cd "$(dirname "$0")"

# Run using virtual environment's Python
./my-venv/bin/python src/main.py
