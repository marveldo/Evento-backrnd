#!/bin/sh
python manage.py makemigrations users events --no-input
python manage.py migrate --no-input
python manage.py runserver 0.0.0.0:8000