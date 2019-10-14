help:
	@echo 'Makefile for managing web application                        '
	@echo '                                                             '
	@echo 'Usage:                                                       '
	@echo ' make build      build images                                '
	@echo ' make rebuild-ui build frontend code                         '
	@echo ' make up         creates containers and starts service       '
	@echo ' make iup        creates containers and runs interactively   '
	@echo ' make start      starts service containers                   '
	@echo ' make stop       stops service containers                    '
	@echo ' make down       stops service and removes containers        '
	@echo '                                                             '
	@echo ' make migrate    run migrations                              '
	@echo ' make test       run tests                                   '
	@echo ' make test_cov   run tests with coverage.py                  '
	@echo ' make test_fast  run tests without migrations                '
	@echo ' make lint       run flake8 linter                           '
	@echo '                                                             '
	@echo ' make attach     attach to process inside service            '
	@echo ' make logs       see container logs                          '
	@echo ' make shell      connect to app container in new bash shell  '
	@echo ' make dbshell    connect to postgres inside db container     '
	@echo ' make load_talks Load talk data into Talks table             '
	@echo '                                                             '

build:
	docker-compose build

up:
	docker-compose up -d

iup:
	# build and run interactively
	docker-compose up --build

start:
	docker-compose start

stop:
	docker-compose stop

down:
	docker-compose down

rebuild: down build up

rebuild-ui:
	cd frontend && yarn build && cd .. &&  \
	docker-compose restart app

attach: ## Attach to app container
	docker attach `docker-compose ps -q app`

logs:
	docker-compose logs -f app

flask_shell: ## Shell into Flask process
	docker-compose exec app flask konch

shell: ## Shell into app container
	docker-compose exec app bash

dbshell: ## Shell into postgres process inside db container
	docker-compose exec db psql -U postgres

migration: up ## Create migrations using flask migrate
	docker-compose exec app flask db migrate -m "$(m)" --directory ./talkvoter/migrations/

migrate: up ## Run migrations using flask migrate
	docker-compose exec app flask db upgrade --directory ./talkvoter/migrations/

migrate_back: up ## Rollback migrations using flask migrate
	docker-compose exec app flask db downgrade --directory ./talkvoter/migrations/

test: migrate
	docker-compose exec app pytest

test_cov: migrate
	docker-compose exec app pytest --verbose --cov

test_cov_view: migrate
	docker-compose exec app pytest --cov --cov-report html && open ./htmlcov/index.html

test_fast: ## Can pass in parameters using p=''
	docker-compose exec app pytest $(p)

load_talks: up
	docker-compose exec app flask load_talks

superuser: up
	docker-compose exec app flask createsuperuser $(username) $(password)


# Flake 8
# options: http://flake8.pycqa.org/en/latest/user/options.html
# codes: http://flake8.pycqa.org/en/latest/user/error-codes.html
lint: up
	docker-compose exec app flake8
