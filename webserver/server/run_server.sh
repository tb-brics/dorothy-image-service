  
#!/usr/bin/env bash

echo "Starting GUnicorn for handling dynamic content."
gunicorn --config gunicorn_config.py dorothy.wsgi &

#Make sure that NGinx is saving its logs to the same path as GUnicorn.
echo "Starting NGinx for serving static content."
nginx -g "daemon off;"