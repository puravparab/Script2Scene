#!/bin/bash

# Check if Poetry is installed
if command -v poetry &> /dev/null; then
    echo "Poetry is already installed."
else
    echo "Installing Poetry..."
    # Install Poetry
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies using Poetry
echo "Installing dependencies..."
poetry install

# Change to the directory where your Flask app is located
cd script2scene

# Export environment variables
export FLASK_APP=app.py

# Run the Flask server
echo "Running Flask server..."
poetry run flask run

# Go back to the original directory
cd ..