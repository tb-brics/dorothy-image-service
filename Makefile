
build:
	@docker build ./webserver/ --tag tbbrics/dorothy-image-service-web:latest --network host

start:
	@docker-compose up