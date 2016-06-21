#! /bin/bash


sleep 5

/venv/bin/python manage.py migrate
/venv/bin/python manage.py refresh_beer_cache
/venv/bin/python manage.py runserver 0.0.0.0:8000
