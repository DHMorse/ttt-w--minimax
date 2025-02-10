#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Created new virtual environment"
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Installed requirements"
else
    echo "Warning: requirements.txt not found"
fi

# Run the main program
python main.py

# Deactivate virtual environment
deactivate