#!/bin/sh
python manage.py makemigrations --no-input
python manage.py wait_for_db
python manage.py migrate --no-input
python manage.py populate_created_at
python manage.py process_tasks