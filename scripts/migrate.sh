#!/bin/sh

# Exit on any error
set -e

echo "Waiting for database..."
while ! python manage.py check --database default > /dev/null 2>&1; do
    sleep 1
done

echo "Database is ready"
echo "Running migrations..."
python manage.py migrate

echo "Migrations completed successfully"
