build:
	docker-compose build

setupdb:
	docker-compose run --service-ports app sh -c '\
		./wait-for-it.sh mysql:3306 --timeout=30 --strict -- \
		&& mysql -h mysql -uroot -proot -e "\
			CREATE DATABASE IF NOT EXISTS wanted CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci; \
			CREATE DATABASE IF NOT EXISTS wanted_test CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" \
	'

up:
	docker-compose up

down:
	docker-compose down --remove-orphans

shell:
	docker-compose run app bash

shell-mysql:
	docker-compose exec mysql mysql -uroot -proot
