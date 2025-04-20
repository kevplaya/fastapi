build:
	docker-compose build

setupdb:
	docker-compose run --service-ports app sh -c "./wait-for-it.sh mysql:3306; mysql -h mysql -uroot -proot -e 'create database if not exists wanted character set utf8mb4 collate utf8mb4_general_ci';"

up:
	docker-compose up

down:
	docker-compose down --remove-orphans

shell:
	docker-compose run app bash

shell-mysql:
	docker-compose exec mysql mysql -uroot -proot
