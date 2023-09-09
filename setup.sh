#!/bin/bash

# Define variables for your project
PROJECT_NAME="backend_Cahlp"
PYTHON_VERSION="3.11"
VENV_DIR="$PROJECT_NAME-env"

# Check if the virtual environment folder exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    # Create a virtual environment
    python$PYTHON_VERSION -m venv $VENV_DIR
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install requirements
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Deactivate the virtual environment when you're done
deactivate
