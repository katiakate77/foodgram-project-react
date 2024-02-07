#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic

# Copy static files
echo "Copy static files"
cp -r /app/collected_static/. /backend_static/

# Apply database migrations
echo "Apply migrations"
python manage.py migrate

# Start gunicorn server
echo "Start server"
gunicorn --bind 0:8000 foodgram_backend.wsgi
