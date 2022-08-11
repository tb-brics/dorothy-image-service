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

#Creating folder for mlflow logs
RUN mkdir -p /var/log/mlflow
RUN chown -R www-data:www-data /var/log/mlflow

# Creating folder to serve as backend storage for mlflow
RUN mkdir -p /service/mlflow/db/
RUN chown -R www-data:www-data /service/mlflow/db/
RUN chmod 775 /service/mlflow/db/
RUN touch /service/mlflow/db/storage.db
RUN chown -R www-data:www-data /service/mlflow/db/storage.db
RUN chmod 775 /service/mlflow/db/storage.db


# Creating folder to serve as artifact root
RUN mkdir -p /service/mlflow/mlruns/
RUN chown -R www-data:www-data /service/mlflow/mlruns/

# Creating folder to serve as artifact
RUN mkdir -p /service/mlflow/artifacts/
RUN chown -R www-data:www-data /service/mlflow/artifacts/


RUN chown -R www-data:www-data /service/mlflow/
RUN chmod 775 /service/mlflow/

COPY gunicorn_config.py ./gunicorn_config.py
RUN chmod -R 755 ./gunicorn_config.py

#Configuring NGINX for handling static contents.
COPY nginx.default /etc/nginx/sites-available/default

# Run mlflow
COPY run_mlflow.sh /service/run_mlflow.sh
RUN chmod -R 755 /service/run_mlflow.sh
RUN chown -R www-data:www-data /service/