# ==========================================
# Movie Analysis Project Makefile
# ==========================================

# Spin up the database container in detached mode using the .env file
db-up:
	docker compose --env-file .env up -d

# Stop and remove the database container
db-down:
	docker compose down

# Check the running status of the database container
db-status:
	docker ps