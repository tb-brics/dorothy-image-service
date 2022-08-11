#!/usr/bin/env bash
echo "Starting NGinx for serving static content."
nginx -g "daemon off;" &
echo "Starting mlflow server"
mlflow server --host 0.0.0.0 --backend-store-uri sqlite:////service/mlflow/db/storage.db \
 --serve-artifacts \
 --default-artifact-root /service/mlflow/mlruns \
 --artifacts-destination /service/mlflow/artifacts \
 --gunicorn-opts "--config ./gunicorn_config.py"