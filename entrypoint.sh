#!/bin/sh
python manage.py makemigrations users events --no-input
python manage.py migrate --no-input
gunicorn evento.wsgi:application --bind 0.0.0.0:8000 --reload
