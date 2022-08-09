#!/usr/bin/env bash
echo "Starting mlflow server"
mlflow server --host 0.0.0.0 --backend-store-uri sqlite:////service/mlflow/db/storage.db \
 --serve-artifacts \
 --default-artifact-root /service/mlflow/mlruns \
 --artifacts-destination /service/mlflow/artifacts \
 --gunicorn-opts "-g www-data -u www-data"