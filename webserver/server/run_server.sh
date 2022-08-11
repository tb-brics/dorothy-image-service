#!/usr/bin/env bash
echo "Starting NGinx for serving static content."
nginx -g "daemon off;" &
echo "starting server"
python manage.py runserver 0.0.0.0:8000
