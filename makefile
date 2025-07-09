## Dev related
# Main commands
run:
	docker-compose -f infra/dev/docker-compose.yml up -d --build
run_follow:
	docker-compose -f infra/dev/docker-compose.yml up --build
down:
	docker-compose -f infra/dev/docker-compose.yml down
build: 
	docker-compose -f infra/dev/docker-compose.yml build

lint:
	black  back/app/ 
	isort back/app/
	pylint back/app/

# Shells
app_shell:
	docker exec -it dev-back-1  /bin/bash 

mongo_shell:
	docker exec -it dev-db-1 mongosh -u techmatch -p techmatch

# Logs
app_log:
	docker-compose -f infra/dev/docker-compose.yml logs back

app_log_follow:
	docker-compose -f infra/dev/docker-compose.yml logs -f back

mongo_log:
	docker-compose -f infra/dev/docker-compose.yml logs db

mongo_log_follow:
	docker-compose -f infra/dev/docker-compose.yml logs -f db
