#! /usr/bin/env bash

set -e
set -x

# Run migrations
echo "Performing database alembic migrations"
alembic upgrade head

# Let the DB start
echo "Running backend_pre_start.py"
python app/backend_pre_start.py

# Create initial data in db
echo "Adding initial data to database"
python app/initial_data.py

