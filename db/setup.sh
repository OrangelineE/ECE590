#!/bin/bash

# Database configuration
DB_USER="postgres"
DB_PASSWORD="passwd123"
DB_NAME="ece590"

# Run the SQL script
export PGPASSWORD=$DB_PASSWORD
psql -U $DB_USER -d $DB_NAME -a -f "init.sql"

# Remove the password from environment
unset PGPASSWORD

echo "Database has been set up and initial data has been loaded."
