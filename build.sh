#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run migrations

python manage.py makemigrations
python manage.py migrate
# Collect static files
python manage.py collectstatic --noinput

python create_superuser.py
