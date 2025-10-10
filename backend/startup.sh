#!/bin/bash

# Run database migrations
python manage.py migrate --noinput

# Start Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 AppName.wsgi

