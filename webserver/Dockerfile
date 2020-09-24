FROM python:3.7

#This will force log messages to not be buffered.
ENV PYTHONUNBUFFERED 1

#Installing SO-level dependencies
RUN apt-get update && apt-get install nginx gettext vim -y --no-install-recommends

#Configuring NGINX for handling static contents.
COPY server/nginx.default /etc/nginx/sites-available/default
#RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

#Setting working environment
WORKDIR /service

#Here is where we will mount the volume containing all the x-ray images
RUN mkdir /imagesrep
RUN chown -R www-data:www-data /imagesrep

#Installing dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

#Copying necessary files for production execution.
COPY django ./

#Creating folder to contain static files.
RUN mkdir -p /var/www/dorothy/static
RUN chown -R www-data:www-data /var/www/dorothy/static

#Copying script that will start GUnicorn and NGinx web servers.
COPY server/run_server.sh ./