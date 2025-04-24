#!/bin/bash

rm db.sqlite3
rm -rf ./apiapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations apiapi
python3 manage.py migrate apiapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

