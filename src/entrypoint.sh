#!/usr/bin/env sh

if [ "$#" = 0 ]
then
    python3.7 -m pip freeze
fi

cd csv_server
if [ "$#" = 0 ]
then
    >&2 echo "No command detected; running default commands"
    >&2 echo "Running migrations"
    python3.7 manage.py makemigrations
    python3.7 manage.py migrate --noinput
    >&2 echo "\n\nStarting development server: 127.0.0.1:8000\n\n"
    python3.7 manage.py runserver 0.0.0.0:8000
else
    >&2 echo "Command detected; running command"
    exec "$@"
fi