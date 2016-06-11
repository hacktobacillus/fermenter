#! /bin/bash


sleep 5

/venv/bin/python manage.py syncdb
/venv/bin/python manage.py migrate
/venv/bin/python manage.py runserver 0.0.0.0:8000