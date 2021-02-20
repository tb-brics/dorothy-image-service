FROM rctorres/dorothy:0.5

#This will force log messages to not be buffered.
ENV PYTHONUNBUFFERED 1

#Currently, the production version (LPS) is mapping /imagesrep to ~torres/Imagens_Temp.
#As a result, /imagesrep within the container is owned to user/group rtorres:rtorres (1419/513)
#Currently, the solution for this is:
# - Create a "dorothy" group with the same ID as "torres" group (513).
# - chown /imagesrep to www-data:dorothy (see below)
# - chmod /imagesrep to 775 (full permission to group members) (see below)
# - chmod ~torres/Imagens_Temp (in the host machine) to 775 (full permission to group members)
RUN groupadd -g 513 dorothy
RUN usermod -a -G dorothy root
RUN usermod -a -G dorothy www-data

#Configuring NGINX for handling static contents.
COPY server/nginx.default /etc/nginx/sites-available/default

#Setting working environment
WORKDIR /service

#Installing dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

#Here is where we will mount the volume containing all the x-ray images
RUN mkdir /imagesrep
RUN chown -R www-data:dorothy /imagesrep
RUN chmod -R 775 /imagesrep

#Creating folder to contain static files.
RUN mkdir -p /software/dorothy/static
RUN chown -R www-data:www-data /software/dorothy/static

#Creating folder for dorothy logs
RUN mkdir -p /var/log/dorothy
RUN chown -R www-data:www-data /var/log/dorothy

#Copying script that will start GUnicorn and NGinx web servers.
COPY server/run_server.sh ./
COPY server/gunicorn_config.py ./

#Copying necessary files for production execution.
COPY django ./

#Setting up Django (static content and messages)
#DO NOT DO THE DB MIGRATION HERE!
RUN python manage.py collectstatic --no-input
#RUN django-admin compilemessages
