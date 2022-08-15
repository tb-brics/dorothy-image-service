
build-image-service:
	@docker build ./webserver/ --tag tbbrics/dorothy-image-service-web:latest --network host

build-mlflow-service:
	@docker build ./mlflow/ --tag tbbrics/dorothy-mlflow-service:latest --network host

build-all:
	$(MAKE) build-image-service
	$(MAKE) build-mlflow-service

start-prod:
	@docker-compose up

start-dev:
	@docker-compose -f docker-compose-dev.yaml up