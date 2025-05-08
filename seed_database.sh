#!/bin/bash

rm db.sqlite3
rm -rf ./apiapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations apiapi
python3 manage.py migrate apiapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata categories
python3 manage.py loaddata questions
python3 manage.py loaddata question_category
python3 manage.py loaddata quiz_attempt
python3 manage.py loaddata quiz_response


