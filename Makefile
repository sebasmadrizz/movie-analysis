# ==========================================
# Movie Analysis Project Makefile
# ==========================================
VENV = .venv
BIN = $(VENV)/bin

# Spin up the database container in detached mode using the .env file
db-up:
	docker compose --env-file .env up -d

# Stop and remove the database container
db-down:
	docker compose down

# Check the running status of the database container
db-status:
	docker ps
	# Create virtual environment and install dependencies
venv:
	python3 -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements.txt

# Run the database connectivity test script
test-db:
	$(BIN)/python tests/db_test.py

# Clean Python cache and virtual environment
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +