#!/bin/sh

set -e  

echo "Running migrations..."
python manage.py makemigrations accounts --noinput 
python manage.py migrate accounts --noinput 
# python manage.py makemigrations core --noinput 
# python manage.py migrate core --noinput
python manage.py makemigrations  --noinput 
python manage.py migrate  --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Server..."
# exec gunicorn -b 0.0.0.0:8000 --workers 3 --timeout 120 config.wsgi:application
exec daphne -b 0.0.0.0 -p 8000 config.asgi:application