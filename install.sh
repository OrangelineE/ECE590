#!/bin/bash

# Resolve the real path to the script and navigate to the directory
mypath=$(realpath "$0")
mybase=$(dirname "$mypath")
cd "$mybase" || exit 1  # Exit if changing directory fails

# Generate a random secret key
SECRET=$(tr -dc 'a-z0-9-_' </dev/urandom | head -c50)
echo "Creating .flaskenv with configuration"
echo "FLASK_APP=pillbox.py
FLASK_DEBUG=True
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
SECRET_KEY='$SECRET'
DB_NAME=ece590
DB_USER=${PGUSER}
DB_PORT=${PGPORT}
DB_HOST=${PGHOST}
DB_PASSWORD=${PGPASSWORD}" > .flaskenv


# Check for Poetry and install if not found
if ! command -v poetry &> /dev/null
then
    echo "Poetry could not be found, installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "Poetry installed successfully."
else
    echo "Poetry is already installed."
fi

# Ensure Poetry is in the path (adjust as necessary for your setup)
export PATH="$HOME/.poetry/bin:$PATH"

# Install Python dependencies using Poetry
echo "Installing dependencies..."
poetry install

# Check if db/setup.sh exists and run it
if [ -f db/setup.sh ]; then
    echo "Running database setup script..."
    bash db/setup.sh
else
    echo "Database setup script not found at db/setup.sh."
fi