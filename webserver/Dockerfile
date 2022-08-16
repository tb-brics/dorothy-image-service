FROM tbbrics/dorothy:0.2

#This will force log messages to not be buffered.
#ENV PYTHONUNBUFFERED 1

#Currently, the production version (LPS) is mapping /imagesrep to
#/datasets/dorothy-image-dorothy-image-imagesrep-nfs-pvc-f87af903-24a8-4020-920e-491f5400ba9c
#As a result, /imagesrep within the container is owned to user/group root:root (1419/513)
#If annuser is added to the group "datasets" (id=10001), the user will have access to the dir above.
#Currently, the solution for this is:
# - Create a "datasets" group with the same ID as "datasets" group (10001).
# - chown /imagesrep to www-data:datasets (see below)
# - chmod /imagesrep to 775 (full permission to group members) (see below)
# - Make sure that /datasets/dorothy-image-dorothy-image-imagesrep-nfs-pvc-f87af903-24a8-4020-920e-491f5400ba9c
#   has group access to "datasets" group
RUN groupadd -g 10001 datasets
RUN usermod -a -G datasets root
RUN usermod -a -G datasets www-data

#Setting working environment
WORKDIR /service

#Installing dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

#Here is where we will mount the volume containing all the x-ray images
RUN mkdir /imagesrep
RUN chown -R www-data:datasets /imagesrep
RUN chmod -R 775 /imagesrep

#
RUN mkdir /imagesrep/clusters
RUN chown -R www-data:datasets /imagesrep/clusters
RUN chmod -R 775 /imagesrep/clusters

#Creating folder to contain static files.
RUN mkdir -p /var/www/dorothy/static/
RUN chown -R www-data:www-data /var/www/dorothy/static/

#Creating folder for dorothy logs
RUN mkdir -p /var/log/dorothy
RUN chown -R www-data:www-data /var/log/dorothy


#Configuring NGINX for handling static contents.
COPY server/nginx.default /etc/nginx/sites-available/default
#COPY ./nginx.default /etc/nginx/nginx.default
#COPY server/nginx.conf /etc/nginx/nginx.conf

#Copying script that will start GUnicorn and NGinx web servers.
COPY server/gunicorn_config.py ./gunicorn_config.py
RUN chmod -R 755 ./gunicorn_config.py
COPY server/run_server.sh ./run_server.sh
RUN chmod -R 755 ./run_server.sh


#Copying necessary files for production execution.
COPY django ./

#Setting up Django (static content and messages)
#DO NOT DO THE DB MIGRATION HERE!
RUN python manage.py collectstatic --no-input
#RUN django-admin compilemessages